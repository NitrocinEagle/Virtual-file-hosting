import boto3


class S3Connector:
    bucket_name = None
    connect = None

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.connect = boto3.resource('s3')
        self.client = boto3.client('s3')
        self.bucket = boto3.resource('s3').Bucket(bucket_name)
        self.objects = self.client.list_objects(Bucket=bucket_name, MaxKeys=1000)

    def get_objects(self):
        return self.objects

    def create_bucket(self):
        self.connect.create_bucket(Bucket=self.bucket_name,
                                   CreateBucketConfiguration={
                                       'LocationConstraint': 'us-west-1'
                                   })

    def upload_file(self, file):
        data = open(file, 'rb')
        self.connect.Bucket(self.bucket_name).put_object(Key=file, Body=data)

    def upload_files(self, files):
        for file in files:
            self.upload_file(file)

    def download_file(self, key, file_name):
        self.client.download_file(self.bucket_name, key, file_name)

    def create_folder(self, name):
        return self.bucket.put_object(Key=name)

    def upload_object(self, data, key):
        self.client.upload_fileobj(data, self.bucket_name, key)

    def update_objects(self):
        self.objects = self.client.list_objects(Bucket=self.bucket_name, MaxKeys=1000)


s3 = S3Connector('justsomeexamplebucket22')
