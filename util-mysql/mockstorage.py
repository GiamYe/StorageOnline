__author__ = 'zhenanye'
import requests
import requests.exceptions as exceptions
from  storage import Storage as Storage


class mock(Storage):
    """
    sheepdog driver
    """

    def __init__(self, url='http://localhost', version='v1', account='ypan', container='ypan'):
        self.URL = url
        self.VERSION = version
        self.ACCOUNT = account
        self.CONTAINER = container

        print '/'.join([self.URL, self.VERSION, self.ACCOUNT])
        print '''request for creating account'''
        print '''request for creating container'''


    def create_object(self, *args, **kwargs):
        print 'create object'
        return True

    def get_object(self, *args, **kwargs):
        print 'read object' + kwargs['uuid']
        return "File content text"

    def update_object(self, *args, **kwargs):
        print 'update object'
        return True

    def delete_object(self, *args, **kwargs):
        print 'delete object'
        return True

