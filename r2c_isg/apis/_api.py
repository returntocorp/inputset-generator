import os
import json
import shutil
import requests
from typing import Optional, Union
from datetime import datetime, timedelta
from hashlib import md5
from abc import ABC, abstractmethod
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from r2c_isg.structures import Project


class Api(ABC):
    def __init__(self, **kwargs):
        self.cache_dir = '.requests_cache'
        self.cache_timeout = timedelta(weeks=1)
        self.nocache = False

        # call update to add any user-modifiable values
        self.update(**kwargs)

    def update(self, **kwargs):
        """Populates the api with data from a dictionary."""
        # set/create the cache dir
        self.cache_dir = kwargs.pop('cache_dir', None) or self.cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # set how long a cached file is valid
        self.cache_timeout = kwargs.pop('cache_timeout', None) \
                             or self.cache_timeout

        # set nocache (can be overridden by individual requests)
        self.nocache = kwargs.pop('nocache', None) or self.nocache

    def request(
            self, url: str, request_type: str = 'get',
            nocache: bool = None, cache_timeout: timedelta = None,
            headers: dict = {}, data: dict = {}, **_
    ) -> (int, Optional[Union[dict, list]]):
        """Loads a url from cache or downloads it from the web."""

        # url + request type + headers + data uniquely identifies a
        # request in the cache
        uuid = '%s%s%s%s' % (url, request_type, str(headers), str(data))
        filename = md5(uuid.encode()).hexdigest()
        filepath = '%s/%s.json' % (self.cache_dir, filename)

        # request-specific nocache setting overrides the api-level setting
        nocache = nocache if nocache is not None else self.nocache
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
                    return cached['status'], cached['json']

        # get/post to request the data (if not loaded from file)
        s = requests.Session()
        # retry 3 times--after 0, 2, and 4 seconds--for basic connection
        # issues (eg, DNS lookup errors) and 502/503/504
        retries = Retry(total=3, backoff_factor=1,
                        status_forcelist=[502, 503, 504])
        # the first arg applies the adapter to only urls matching that
        # prefix; in this case, we want to match all urls, so we use ''
        s.mount('', HTTPAdapter(max_retries=retries))
        try:
            if request_type == 'post':
                r = s.post(url, headers=headers, data=json.dumps(data))
            else:
                r = s.get(url, headers=headers, data=json.dumps(data))
        except KeyboardInterrupt:
            # allow ctrl-c to cancel the request
            raise
        except:
            print('Warning: Could not load %s.' % url)
            # 0 status code means error
            return 0, None

        # get response json
        try:
            data = r.json()
        except json.JSONDecodeError as e:
            print('Warning: Non-json response from %s.' % url)
            # 0 status code means error
            return 0, None

        # save the response json to cache (only 2xx response codes are cached)
        if r.status_code in range(200, 300):
            with open(filepath, 'w') as json_file:
                cached = {
                    'url': url,
                    'status': r.status_code,
                    'timestamp': datetime.utcnow(),
                    'json': data
                }
                json.dump(cached, json_file, indent=4, default=str)

        return r.status_code, data

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
        return self.__class__.__name__
