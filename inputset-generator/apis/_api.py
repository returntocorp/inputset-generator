import os
import json
import requests
from typing import Union
from datetime import datetime, timedelta
from hashlib import md5
from abc import ABC, abstractmethod

from structures import Project


class Api(ABC):
    def __init__(self):
        # set/create the cache dir
        self.cache_dir = 'cache'
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # set how long a cached file is valid
        self.cache_timeout = timedelta(weeks=1)

    def request(self, url: str, **headers) -> Union[dict, list]:
        """Loads a url from cache or downloads it from the web."""

        # try loading the data from the cache
        filename = md5(url.encode()).hexdigest()
        filepath = '%s/%s.json' % (self.cache_dir, filename)

        if os.path.isfile(filepath):
            # load the file from disk
            cached = json.load(open(filepath))
            cached_date = datetime.strptime(cached['timestamp'],
                                            '%Y-%m-%d %H:%M:%S.%f')

            if datetime.utcnow() < cached_date + self.cache_timeout:
                # cached data isn't too old; return it
                return cached['json']

        # download the url
        try:
            r = requests.get(url, headers=headers)
            data = r.json()
            if r.status_code != 200:
                raise Exception('Exception: %s' % str(data))

        except:
            raise Exception('Error: No response or non-json response'
                            ' for url %s.' % url)

        # save the response json to cache
        with open(filepath, 'w') as json_file:
            cached = {
                'timestamp': datetime.utcnow(),
                'json': data
            }
            json.dump(cached, json_file, indent=4, default=str)

        return data

    def clean_cache(self, url):
        """Deletes the cache file associated with this url."""

        # find the file and delete it
        filename = md5(url.encode()).hexdigest()
        filepath = '%s/%s.json' % (self.cache_dir, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)

    @abstractmethod
    def get_project(self, project: Project) -> None: pass

    @abstractmethod
    def get_versions(self, project: Project,
                     hist: str = 'all') -> None: pass
