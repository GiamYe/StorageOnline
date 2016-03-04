__author__ = 'zhan'
import logging
from storage import Storage as Storage
from boto3.session import Session

class S3(Storage):

    logger = logging.getLogger(__name__)

    def __init__(self, access_key, access_secret, region, bucket='ypanbucket'):
        session = Session(aws_access_key_id=access_key,
                            aws_secret_access_key=access_secret,
                            region_name=region)

        self.client = session.client('s3')
        self.bucket = bucket

    def create_object(self, *args, **kwargs):
        try:
            file = kwargs.get('file')
            content = kwargs.get('content')
            uuid = kwargs.get('uuid')

            if file:
                f = open(file, 'rb')
                content = f.read()

            return self.client.put_object(Body=content, Bucket=self.bucket, Key=uuid)
        except IndexError:
            self.logger.error('missing parameter, please make sure  {uuid} parameter is specified')

        except IOError:
            self.logger.error('failed to open file for uploading, please make sure the file has been put into \
                              the temp folder')

    def get_object(self, *args, **kwargs):
        try:
            uuid = kwargs.get('uuid')
            response = self.client.get_object(Bucket=self.bucket, Key=uuid)
            return response['Body'].read()

        except IndexError:
            self.logger.error('missing parameter, please make sure  {uuid} parameter is specified')

    def delete_object(self, *args, **kwargs):
        try:
            uuid = kwargs.get('uuid')
            return self.client.delete_object(Bucket=self.bucket, Key=uuid)
        except IndexError:
            self.logger.error('missing parameter, please make sure  {uuid} parameter is specified')








