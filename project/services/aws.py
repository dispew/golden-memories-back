import boto3
from botocore.exceptions import NoCredentialsError


class AWSS3:

    def __init__(self, app, bucket):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=app.config['S3_ACCESS_KEY'],
            aws_secret_access_key=app.config['S3_SECRET_KEY'])
        self.bucket = bucket

    def upload_to_aws(self, file_object, s3_file_key):
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

    def list_bucket(self):
        try:
            print("List Successful")
            return self.s3.list_objects(Bucket=self.bucket)['Contents']
        except NoCredentialsError:
            print("Credentials not available")
            return None
        except Exception as ex:
            print(ex)
            return False

    def gen_temp_url(self, key):
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
            return False
