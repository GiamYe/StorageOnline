__author__ = 'zhenanye'
import requests
import requests.exceptions as exceptions
from storage import Storage as Storage
import logging

class SheepDog(Storage):
    """
    sheepdog driver
    """

    logger = logging.getLogger(__name__)

    def __init__(self, url='http://localhost', version='v1', account='ypan', container='ypan'):
        '''
        :param url:
        :param version:
        :param account:
        :param container:
        :return:
        '''
        self.URL = url
        self.VERSION = version
        self.ACCOUNT = account
        self.CONTAINER = container

        self.logger.debug('initialize connection to %s' %('/'.join([self.URL, self.VERSION, self.ACCOUNT])))

        # check for creating account in case this is the first time application started.
        try:
            print '/'.join([self.URL, self.VERSION, self.ACCOUNT])
            r = requests.put('/'.join([self.URL, self.VERSION, self.ACCOUNT]), timeout=30)

            if not r.ok:
                self.logger.error('account creation/confirmation failed')
                raise IOError('Connect to sheepdog storage failed')
        except exceptions.Timeout:
            self.logger.error('connect to sheepdog timeout')
            raise IOError('Connect to sheepdog storage failed')

        # check for creating container in case this is the first time user registered.
        try:
            r = requests.put('/'.join([self.URL, self.VERSION, self.ACCOUNT, self.CONTAINER]))
            if not r.ok:
                self.logger.error('container creation confirmation failed')
                raise IOError('Connect to sheepdog storage failed')
        except exceptions.Timeout:
            self.logger.error('connect to sheepdog timeout')
            raise IOError('Connect to sheepdog storage failed')

    def create_object(self, *args, **kwargs):
        try:
            file = kwargs.get('file')
            content = kwargs.get('content')
            uuid = kwargs.get('uuid')

            if file:
                f = open(file, 'rb')
                content = f.read()

            r = requests.put('/'.join([self.URL, self.VERSION, self.ACCOUNT, self.CONTAINER, uuid]), data=content)
            if r.ok:
                return True
        except IndexError:
            self.logger.error('missing parameter, please make sure both {file} and {uuid} parameter are \
            specified')
            return False
        except IOError:
            self.logger.error('failed to open file for uploading, please make sure the file has been put into \
                              the temp folder')
            return False
        except exceptions.Timeout:
            self.logger.error('connect to sheepdog timeout')
            raise IOError('Connect to sheepdog storage failed')

    def get_object(self, *args, **kwargs):
        try:
            uuid = kwargs.get('uuid')
            if not uuid:
                uuid = args[0]

            r = requests.get('/'.join([self.URL, self.VERSION, self.ACCOUNT, self.CONTAINER, uuid]))
            if r.ok:
                return r.content
        except IndexError:
            self.logger.error('missing parameter, please make sure {uuid} parameter is specified')
            return False
        except exceptions.Timeout:
            self.logger.error('connect to sheepdog timeout')
            raise IOError('Connect to sheepdog storage failed')

    def update_object(self, *args, **kwargs):
        try:
            file = kwargs.get('file')
            uuid = kwargs.get('uuid')
            content = kwargs.get('content')

            if file:
                f = open(file, 'rb')
                content = f.read()
            r = requests.put('/'.join([self.URL, self.VERSION, self.ACCOUNT, self.CONTAINER, uuid]), data=content)
            if r.ok:
                return True
        except IndexError:
            self.logger.error('missing parameter, please make sure {uuid} parameter is specified')
            return False
        except IOError:
            self.logger.error('failed to open file for uploading, please make sure the file has been put into \
                              the temp folder')
            return False
        except exceptions.Timeout:
            self.logger.error('connect to sheepdog timeout')
            raise IOError('Connect to sheepdog storage failed')

    def delete_object(self, *args, **kwargs):
        try:
            uuid = kwargs.get('uuid')
            if not uuid:
                uuid = args[0]

            r = requests.delete('/'.join([self.URL, self.VERSION, self.ACCOUNT, self.CONTAINER, uuid]))
            if r.ok:
                return True
        except IndexError:
            self.logger.error('missing parameter, please make sure  {uuid} parameter is specified')
            return False
        except exceptions.Timeout:
            self.logger.error('connect to sheepdog timeout')
            raise IOError('Connect to sheepdog storage failed')

