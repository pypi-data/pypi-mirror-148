
import json
import os

import boto3
import pandas as pd
from dask import dataframe as dd
from pyathena import connect

# TODO: migrate these to environment variables
ACCESS_KEY = os.environ.get("ATHENA_ACCESS_KEY")
SECRET_KEY = os.environ.get("ATHENA_SECRET_KEY")
SERIAL_NUMBER = os.environ.get("ATHENA_SERIAL_NUMBER")

S3_STAGING_DIR = "s3://aws-athena-query-results-268919952580-us-east-1/"
BUCKET = "aws-athena-query-results-268919952580-us-east-1"
REGION_NAME = "us-east-1"
SCHEMA_NAME = 'cornershop_warehouse'

class AWSS3Wrapper:

    def __init__(self, region_name: str = "us-east-1"):
        self._s3 = boto3.resource(
            's3',
            region_name = region_name,
            aws_access_key_id = (ACCESS_KEY),
            aws_secret_access_key = (SECRET_KEY),
        )

    def get_list_of_prefixes_from_prefix(self, bucket, prefix, delimiter = "/"):
        """gets list of prefixes for given bucket and prefix"""
        list_of_prefixes = []
        paginator = self._s3.meta.client.get_paginator('list_objects')
        for result in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter=delimiter):
            if 'CommonPrefixes' in result:
                prefixes = [f['Prefix'] for f in result['CommonPrefixes']]
                list_of_prefixes.extend(prefixes)
        return list_of_prefixes

    def download(self, bucket, prefix, path):
        bucket_obj = self._s3.Bucket(bucket)
        bucket_obj.download_file(prefix, path)

    def read_json(self, bucket_name, file_path):
        content_object = self._s3.Object(bucket_name, file_path)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        return json.loads(file_content)

    def write_json(self, object_to_write, bucket_name: str, file_path: str):
        # Write buffer to S3 object
        self._s3.Object(bucket_name, file_path).put(
            Body = (bytes(json.dumps(object_to_write).encode('UTF-8')))
        )
        return f"https://{bucket_name}.s3.amazonaws.com/{file_path}"

    def write_html(self, html_to_write: str, bucket_name: str, file_path: str):
        # Write buffer to S3 object
        self._s3.Object(bucket_name, file_path).put(
            Body = html_to_write,
            ContentType = 'text/html'
        )
        return f"https://{bucket_name}.s3.amazonaws.com/{file_path}"


class RemoteDataFrame:

    def __init__(self, s3_dir: str):
        assert (
            "s3://" in s3_dir
            and s3_dir[0:5] == "s3://"
            and len(s3_dir.strip("s3://").split("/"))>1
        ), "s3_dir should be a valid s3 path (s3://BUCKET_NAME/...)"
        self.s3_dir = s3_dir
        self.aws_access_key_id = ACCESS_KEY
        self.aws_secret_access_key = SECRET_KEY
        self.aws_s3_wrapper = AWSS3Wrapper()

    @property
    def bucket(self):
        return self.s3_dir.strip("s3://").split("/")[0]

    @property
    def prefix(self):
        return "/".join(self.s3_dir.strip("s3://").split("/")[1:])

    def download(self, path):
        self.aws_s3_wrapper.download(bucket = self.bucket, prefix = self.prefix, path = path)
        return lambda : pd.read_csv(path)

    def compute(self):
        """
        returns a pandas dataframe
        """
        df = dd.read_csv(
            self.s3_dir,
            storage_options = {
                'key': self.aws_access_key_id,
                'secret': self.aws_secret_access_key
            },
            assume_missing=True
        )
        return df.compute()

    def __call__(self):
        return self.compute()

    def __str__(self):
        return self.s3_dir


class AthenaWrapper:
    '''
    # lazy execution usage example
    lazy_df = athena_wrapper.execute("""
        SELECT *
        FROM "cornershop_warehouse"."orders_order"
        LIMIT 5
        ;
    """, lazy = True)
    print(lazy_df)
    >s3://cornershop-datascience/development/data/raw/74b0990c-f9c7-4091-b3c5-ff53921d916f.csv
    # the query was executed and stored in s3 but it wasn't downloaded as a dataframe or csv file
    df = lazy_df() # this will create a pandas dataframe with the query result
    ---
    # lazy execution donwload csv example
    # if the query result is too big, it is better to download the result first as a csv
    lazy_df.download('orders.csv')
    # we can also load this final csv into the notebook as a dataframe
    df = lazy_df.download('orders.csv')() # don't forget the '()'
    '''
    def __init__(self, schema_name=SCHEMA_NAME):
        print(ACCESS_KEY)
        print(SECRET_KEY)
        print(SERIAL_NUMBER)
        self.aws_access_key_id = ACCESS_KEY
        self.aws_secret_access_key = SECRET_KEY
        self.serial_number = SERIAL_NUMBER
        self.s3_staging_dir = S3_STAGING_DIR # "s3://cornershop-datascience/development/data/raw/"
        self.bucket = BUCKET #"cornershop-datascience"
        self.region_name = REGION_NAME
        self.schema_name = schema_name
        self.cursor = connect(
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            serial_number = self.serial_number,
            s3_staging_dir = self.s3_staging_dir,
            region_name = self.region_name,
            schema_name = self.schema_name
        ).cursor()

    def describe(self, table: str):
        return self.execute(f"""
            SELECT *
            FROM {table}
            LIMIT 5
            ;
        """).dtypes

    def execute(self, query: str, lazy = False):
        cursor = self.cursor.execute(query)
        query_output_location = cursor.output_location
        # location in s3
        remote_df = RemoteDataFrame(s3_dir=query_output_location)
        if lazy:
            return remote_df
        else:
            return remote_df.compute()


