from io import BufferedReader
from typing import Union, Iterable

import boto3
from botocore.exceptions import NoCredentialsError


class AWSS3:

    def __init__(self, config: dict, bucket: str):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=config['S3_ACCESS_KEY'],
            aws_secret_access_key=config['S3_SECRET_KEY'])
        self.bucket = bucket

    def upload_to_aws(self, file_object: BufferedReader, s3_file_key: str) -> bool:
        """Uploads a file to AWS S3 Bucket

        :type file_object: BufferedReader
        :param file_object: The file handler
        :type s3_file_key: str
        :param s3_file_key: The AWS S3 file key identifier

        :returns: The presigned url
        """
        try:
            self.s3.upload_fileobj(Fileobj=file_object, Bucket=self.bucket, Key=s3_file_key)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except Exception as ex:
            print(ex)
            return False

    def list_bucket(self) -> Union[Iterable[dict], None]:
        """List all files in the S3 Bucket

        :returns: List of dictionarys describing the files
        """
        try:
            print("List Successful")
            return self.s3.list_objects(Bucket=self.bucket)['Contents']
        except NoCredentialsError:
            print("Credentials not available")
            return None
        except Exception as ex:
            print(ex)
            return None

    def gen_temp_url(self, key: str) -> Union[str, None]:
        """Generates a presigned url

        :type key: str
        :param key: The AWS S3 file key identifier

        :returns: The presigned url
        """
        try:
            return self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=100)
        except NoCredentialsError:
            print("Credentials not available")
            return None
        except Exception as ex:
            print(ex)
            return None
