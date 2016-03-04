__author__ = 'zhenanye'
from exceptions import NotImplementedError as NotImplementedError

class Storage():
    def __init__():
        pass

    def get_object(self, *args, **kwargs):
        raise NotImplementedError

    def update_object(self, *args, **kwargs):
        raise NotImplementedError

    def delete_object(self, *args, **kwargs):
        raise NotImplementedError

    def create_object(self, *args, **kwargs):
        raise NotImplementedError


def get_storage(type, **kwargs):

    #container = kwargs['uid']

    if type == 'sheepdog':
        modules = __import__('sheepdog')
        sheepdog = getattr(modules, 'SheepDog')

        # return sheepdog(url='http://172.16.9.201', container=container)
        return sheepdog(url='http://172.16.9.201')

    if type == 'awss3':
        modules = __import__('awss3')
        s3 = getattr(modules, 'S3')

        return s3(access_key='AKIAIBPQJ24ZFGVVCCCA',
                  access_secret='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',
                                region='ap-southeast-1')

    if type == 'mock':
        modules = __import__('mockstorage')
        mock = getattr(modules, 'mock')

        return mock()

