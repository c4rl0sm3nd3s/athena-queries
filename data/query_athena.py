import time
import pandas as pd
import io
import config
from data.aws_connection import AWSConnection
from botocore.exceptions import ClientError

class QueryAthena:

    def __init__(self, query):
        self.database = config.athena_db
        self.folder = config.athena_s3folder
        self.bucket = config.athena_bucket 

        self.s3_output =  's3://' + self.bucket + '/' + self.folder
        self.session = AWSConnection(config.aws_profile)

        self.query = query

    def load_conf(self, q):
        try:
            self.client = self.session.get_client('athena')

            response = self.client.start_query_execution(
                QueryString = q,
                    QueryExecutionContext={
                    'Database': self.database
                    },
                    ResultConfiguration={
                    'OutputLocation': self.s3_output,
                    }
            )
            self.filename = response['QueryExecutionId']
            print('Execution ID: ' + response['QueryExecutionId'])

        except ClientError as e:
            print(e)
        return response                

    def run_query(self):
        queries = [self.query]
        for q in queries:
            res = self.load_conf(q)
        try:              
            query_status = None
            while query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None:
                query_status = self.client.get_query_execution(QueryExecutionId=res["QueryExecutionId"])['QueryExecution']['Status']['State']
                print(query_status)
                if query_status == 'FAILED' or query_status == 'CANCELLED':
                    raise Exception('Athena query with the string "{}" failed or was cancelled'.format(self.query))
                time.sleep(10)
            print('Query "{}" finished.'.format(self.query))

            df = self.obtain_data()
            return df

        except ClientError as e:
            print(e)      

    def obtain_data(self):
        try:
            self.resource = self.session.get_resource('s3')

            response = self.resource \
            .Bucket(self.bucket) \
            .Object(key= self.folder + self.filename + '.csv') \
            .get()

            return pd.read_csv(io.BytesIO(response['Body'].read()), encoding='utf8')   
        except Exception as e:
            print(e)  
