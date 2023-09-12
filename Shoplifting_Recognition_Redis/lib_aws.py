import boto3
from boto3.dynamodb.conditions import Key
from lib_init import *


########### Variables #############

AWS_ACCESSKEY="AKIATVLJHPSRQZPX2QLY"
AWS_SECRETKEY="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"
TABLE_NAME="trackerdb"
NOTIFY_TABLE_NAME="notifydb"
BUCKET="inq-ai-tracking"
NOTIFY_BUCKET="inq-ai-notify"
CONFIG_TABLE_NAME="nodeconfig"

###############################

######### AWS #####################


session = boto3.Session(
	aws_access_key_id=AWS_ACCESSKEY,
	aws_secret_access_key=AWS_SECRETKEY,
	region_name='af-south-1'
)
client = boto3.client('s3',aws_access_key_id=AWS_ACCESSKEY, aws_secret_access_key=AWS_SECRETKEY,region_name="af-south-1")
client_ref1= boto3.resource('s3',aws_access_key_id=AWS_ACCESSKEY, aws_secret_access_key=AWS_SECRETKEY,region_name="af-south-1")
client_ref = boto3.client('s3',aws_access_key_id=AWS_ACCESSKEY, aws_secret_access_key=AWS_SECRETKEY,region_name="af-south-1")
if IS_S3=="True":
	client_s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESSKEY, aws_secret_access_key=AWS_SECRETKEY,region_name="af-south-1")
	client_s3_ref1= boto3.resource('s3',aws_access_key_id=AWS_ACCESSKEY, aws_secret_access_key=AWS_SECRETKEY,region_name="af-south-1")
	cli_bucket=client_s3_ref1.Bucket(CUSTOMER_BUCKET)
ref_bucket=client_ref1.Bucket(REF_BUCKET)
dynamodb = session.resource('dynamodb')
table= dynamodb.Table(TABLE_NAME)
notify_table=dynamodb.Table(NOTIFY_TABLE_NAME)
config_table=dynamodb.Table(CONFIG_TABLE_NAME)

lambda_client = boto3.client('lambda', aws_access_key_id=AWS_ACCESSKEY, aws_secret_access_key=AWS_SECRETKEY, region_name="af-south-1")


##########################