# ES-snapshot-restore

Create new ES domain, make sure    Enable fine-grained access control not selected 

[ec2-user@ip-10-224-80-66 ~]$ aws sts get-caller-identity
{
    "Account": "878190441514",
    "UserId": "AROA4Y6B2WQVNJAVOTRN3:i-0dc10dac27b650642",
    "Arn": "arn:aws:sts::878190441514:assumed-role/es-full-access/i-0dc10dac27b650642"
}
[ec2-user@ip-10-224-80-66 ~]$ python3  register-repo.py 
please check https://github.com/xiongye77/ES-snapshot-restore/blob/main/register-repo.py  to register S3 bucket as backup repo. 


Take manual snapshot to snapshot repo

curl -XPUT 'https://search-dev-dcp-tracking-fjzetyjsvg6f5j3sdv6tz226he.ap-southeast-2.es.amazonaws.com/_snapshot/my-snapshot-repo/2022-03-25'

check snapshot status by 
aws s3 ls s3://elasticsearch-backup-878190441514/
curl -XGET "https://search-dev-dcp-tracking-fjzetyjsvg6f5j3sdv6tz226he.ap-southeast-2.es.amazonaws.com/_snapshot/_status"
curl -XGET 'https://search-dev-dcp-tracking-fjzetyjsvg6f5j3sdv6tz226he.ap-southeast-2.es.amazonaws.com/_snapshot/my-snapshot-repo/_all?pretty'


After snapshot finished, change register-repo.py , ES endpoint to a new ES cluster and rerun the command to register again. 

curl -XDELETE 'https://vpc-es-staging-test-kqdrpnsmkracvilguzir37sthi.ap-southeast-2.es.amazonaws.com/_all' delete all items on new created ES cluster
curl -XPOST 'https://vpc-es-staging-test-kqdrpnsmkracvilguzir37sthi.ap-southeast-2.es.amazonaws.com/_snapshot/my-snapshot-repo/2022-03-25/_restore' perform restore. 

Role es-full-access  has 3 policy document 

First is es-full-access

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "es:ESHttpDelete",
                "es:ESHttpGet",
                "es:ESHttpHead",
                "es:ESHttpPost",
                "es:ESHttpPut"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
 }

Second is elasticsearch-backup-878190441514-access allow it to access S3 bucket 

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::elasticsearch-backup-878190441514/*",
                "arn:aws:s3:::elasticsearch-backup-878190441514/"
            ]
        }
    ]
}

Third is es-full-access-iam-passrole 

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::878190441514:role/es-full-access"
        }
    ]
}
