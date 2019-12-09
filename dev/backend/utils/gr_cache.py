""" Module cache """
from os import environ
import redis
from redis.sentinel import Sentinel
from dotenv import load_dotenv, find_dotenv
from flask import request, current_app
__expires__ = environ.get("EXPIRES", 60 * 60 * 24)

try:
    load_dotenv(find_dotenv())
except IOError as exception:
    pass

class Cache:
    """ Cache basic class """
    cache = None
    __type__ = None
    app = current_app

    def __init__(self, app):
        if app:
            self.app = app
        else:
            self.app = current_app
        self.app.qc_cache = self

    def get(self, key):
        """ should return the value of a key in cache"""
        raise NotImplementedError

    def search(self, query):
        """ should return the list of key:value that match the query in cache"""
        raise NotImplementedError

    def save(self, key, value):
        """ should save the value of a key in cache"""
        raise NotImplementedError

    def delete(self, key):
        """ should delete the value of a key in cache"""
        raise NotImplementedError

    def clear(self, pattener):
        """ should clear ALL values from cache that match the pattener"""
        raise NotImplementedError

    def exists(self, key):
        """ should return a bool if the key exists in cache"""
        raise NotImplementedError

    def close(self):
        """ should close the connection with the cache"""
        raise NotImplementedError

class RedisCache(Cache):
    """ Redis Cache """
    __type__ = 'Redis'
    sentinel = None
    master = None
    slave = None
    service_name = ''

    def __init__(self, app, host=environ.get("REDIS", 'redis'), db=0):
        super(RedisCache, self).__init__(app)
        self.cache = redis.Redis(host=host, db=db)
        try:
            self.cache.ping()
            self.app.logger.info('Got a Redis 👍')
        except Exception:
            self.service_name = environ.get("SENTINEL_NAME", 'mymaster')
            self.sentinel = Sentinel([(host, 26379)])
            try:
                self.sentinel.discover_master(self.service_name)
                self.app.logger.info('Got a Sentinel Redis 👌')
                self.__type__ = 'Sentinel'
                self.master = self.sentinel.master_for(self.service_name)
                self.cache = self.sentinel.slave_for(self.service_name)
            except Exception:
                self.app.logger.error('Redis not found')
                self.cache = {}
                self.__type__ = 'Dict'
        self.__redis__ = self.cache
        self.app.gr_cache = self
        if self.cache:
            self.app.redis = self.cache

    def get(self, key):
        try:
            use_cache = int(request.headers.get('QC-Cache', True))
        except RuntimeError:
            use_cache = True
        if not use_cache:
            self.app.logger.warning('Requested to not use cache')
            return None
        return self.cache.get(key)

    def set(self, key, value, ex=__expires__):
        """ set a key """
        return self.save(key, value, ex)

    def search(self, query):
        if isinstance(self.cache, redis.client.Redis):
            keys = self.cache.keys(query)
            values = self.cache.mget(keys)
            return dict(zip(keys, values))
        self.app.logger.error('Not using a Redis to cache')
        return {}
    #pylint: disable=arguments-differ
    def save(self, key, value, ex=__expires__):
        try:
            header_cache = int(request.headers.get('QC-Cache', ex))
        except RuntimeError:
            header_cache = ex
        if not header_cache:
            self.app.logger.warning('Requested to not use cache')
            return True
        if isinstance(self.cache, redis.client.Redis):
            result = self.cache.set(key, value, ex=ex)
            # purge dirty pages
            # self.cache.memory_purge()
            self.app.logger.debug('key %s created', key)
            return result
        self.app.logger.error('Redis not found to save value')
        self.cache[key] = value
        return False
    #pylint: enable=arguments-differ

    def delete(self, key):
        if isinstance(self.cache, redis.client.Redis):
            # purge dirty pages
            # self.cache.memory_purge()
            self.app.logger.debug('key %s deleted', key)
            return self.cache.delete(key)
        try:
            return self.cache.pop(key)
        except Exception:
            return ''

    def clear(self, pattener='*'):
        count = 0
        if isinstance(self.cache, redis.client.Redis):
            keys = self.cache.scan(match=pattener)[1]
            for k in keys:
                count += self.cache.delete(k)
            # purge dirty pages
            self.cache.memory_purge()
        else:
            count = len(self.cache.keys())
            self.cache = {}
        self.app.logger.debug('deleted %d keys', count)
        return count

    def exists(self, key):
        if isinstance(self.cache, redis.client.Redis):
            return bool(self.cache.exists(key))
        return key in self.cache.keys()

    def close(self):
        pass
