import boto3
import requests
from requests_aws4auth import AWS4Auth
#host = 'https://vpc-es-staging-test-kqdrpnsmkracvilguzir37sthi.ap-southeast-2.es.amazonaws.com/'
host = 'https://search-dev-dcp-tracking-fjzetyjsvg6f5j3sdv6tz226he.ap-southeast-2.es.amazonaws.com/'
region = 'ap-southeast-2' # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
print (awsauth)
# Register repository
path = '_snapshot/my-snapshot-repo' # the Elasticsearch API endpoint
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": "elasticsearch-backup-878190441514",
    "region": "ap-southeast-2",
    "role_arn": "arn:aws:iam::878190441514:role/es-full-access"
  }
}

headers = {"Content-Type": "application/json"}

r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)
