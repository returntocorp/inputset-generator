import os
import json
import shutil
import requests
from typing import Union
from datetime import datetime, timedelta
from hashlib import md5
from abc import ABC, abstractmethod

from structures import Project


class Api(ABC):
    def __init__(self, cache_dir: str = 'cache',
                 cache_timeout: timedelta = timedelta(weeks=1), **_):
        # set/create the cache dir
        self.cache_dir = cache_dir or 'cache'
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # set how long a cached file is valid
        self.cache_timeout = cache_timeout or timedelta(weeks=1)

    def request(self, url: str, request_type: str = 'get',
                nocache: bool = False, cache_timeout: timedelta = None,
                headers: dict = {}, data: dict = {}, **_) -> Union[dict, list]:
        """Loads a url from cache or downloads it from the web."""

        # url + request type + headers + data uniquely identifies a
        # request in the cache
        uuid = '%s%s%s%s' % (url, request_type, str(headers), str(data))
        filename = md5(uuid.encode()).hexdigest()
        filepath = '%s/%s.json' % (self.cache_dir, filename)

        if not nocache:
            # try loading the data from cache
            # use default cache timeout if caller hasn't provided one
            cache_timeout = cache_timeout or self.cache_timeout
            if os.path.isfile(filepath):
                # load the file from disk
                cached = json.load(open(filepath))
                cached_date = datetime.strptime(cached['timestamp'],
                                                '%Y-%m-%d %H:%M:%S.%f')

                if datetime.utcnow() < cached_date + cache_timeout:
                    # cached data isn't too old; return it
                    return cached['json']

        # download the url (if not loaded from file)
        try:
            # get/post request the data (default is get)
            if request_type == 'post':
                r = requests.post(url, headers=headers, data=json.dumps(data))
            else:
                r = requests.get(url, headers=headers, data=json.dumps(data))

            # check for non-2xx (error) response codes
            if r.status_code // 100 != 2:
                raise Exception('Exception: %s' % str(data))

            # get response json
            data = r.json()

        except:
            raise Exception('No response or non-json response for url '
                            '%s.' % url)

        # save the response json to cache
        with open(filepath, 'w') as json_file:
            cached = {
                'timestamp': datetime.utcnow(),
                'json': data
            }
            json.dump(cached, json_file, indent=4, default=str)

        return data

    def clear_cache(self):
        """Deletes all cached files."""
        shutil.rmtree(self.cache_dir)
        os.mkdir(self.cache_dir)

    @abstractmethod
    def get_project(self, project: Project, **kwargs) -> None: pass

    @abstractmethod
    def get_versions(self, project: Project,
                     hist: str = 'all', **kwargs) -> None: pass

    def __repr__(self):
        return 'Api(%s)' % self.__class__.__name__
