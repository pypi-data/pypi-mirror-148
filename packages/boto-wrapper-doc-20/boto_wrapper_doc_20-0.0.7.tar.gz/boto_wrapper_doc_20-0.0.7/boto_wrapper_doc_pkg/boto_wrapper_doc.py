from getenv import env
import boto3

class sns_client:
    def create_sns_message(self, topic_id, data):
        key = env["key"]
        secret = env["secret"]
        #bucket_location = env["region"]
        client = boto3.client('sns',aws_access_key_id=key,aws_secret_access_key=secret)
        response =client.publish(TopicArn= topic_id, Message=data)
        return response

ALLOWED_EXTENSIONS = set(['pdf'])

class s3_client:
    def valid_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_document(self, inp_file_name, s3_bucket_name, object_name):
        key = env["key"]
        secret = env["secret"]
        bucket_location = env["region"]
        client = boto3.client('s3',aws_access_key_id=key,aws_secret_access_key=secret)
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location,
            s3_bucket_name,
            object_name)
            
        response = client.upload_file(inp_file_name, s3_bucket_name, object_name,
            ExtraArgs={"Tagging": "public%3Dyes"})
        print(response)
        return response, object_url
        
class cognito_client:
    @staticmethod
    def get_user(sub):
        userpool_id = env["userpool_id"]
        request = {        
            "AttributesToGet": [ "email", "given_name", "family_name" ],
            "Filter": f"sub=\"{sub}\"",
            "UserPoolId": userpool_id
        }
        key = env["key"]
        secret = env["secret"]
        region = env["region"]
        try:
            client = boto3.client('cognito-idp',aws_access_key_id=key,aws_secret_access_key=secret, region_name = region)
        
            response = client.list_users(UserPoolId = request['UserPoolId'], AttributesToGet = request['AttributesToGet'], Filter = request['Filter'])
            user = response["Users"][0]
            username = user["Username"]
            role_response = client.admin_list_groups_for_user(Username=username,UserPoolId=userpool_id)
            role = role_response["Groups"][0]["GroupName"]
            user["role"] = role
        
            return user
        except Exception as e: 
            print(e)
            raise ValueError(f'Error occurred during cognito query {e}')
        
        