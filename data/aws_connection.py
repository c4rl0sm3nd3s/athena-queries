import boto3


class AWSConnection:
    
    def __init__(self, profile):

        self.session = boto3.Session(profile_name=profile)


    def get_client(self, service):
        return self.session.client(service)

    def get_resource(self, service):
        return self.session.resource(service)