import os
import time
import json
import base64
import linecache
import sys
import argparse
import requests
from decimal import Decimal
import hashlib
import threading
from copy import deepcopy


############## Input Variables #############

inq_parser = argparse.ArgumentParser(description='Run EdgeAI detectors')
inq_parser.add_argument("--organization", type=str, nargs="?", default="all")
inq_parser.add_argument("--camid", type=str, nargs="?", default="none")
inq_parser.add_argument("--skiporg", type=str, nargs="?", default="none")
inq_parser.add_argument('--threshold', type=int, nargs="?", default=120)
inq_parser.add_argument('--token', type=str, nargs="?", default="ea002adff538c8136e96949348d2ac812c0052fb")
inq_parser.add_argument('--redis_host', type=str, nargs="?", default="172.17.0.1")
inq_parser.add_argument('--redis_port', type=str, nargs="?", default="6379")
inq_parser.add_argument('--ext_redis_host', type=str, nargs="?", default="172.17.0.1")
inq_parser.add_argument('--ext_redis_port', type=str, nargs="?", default="6379")
inq_parser.add_argument('--s3', type=str, nargs="?", default="False")
inq_parser.add_argument('--bucket', type=str, nargs="?", default="none")
inq_parser.add_argument('--counter', type=str, nargs="?", default="False")
inq_parser.add_argument('--transmit', type=str,nargs="?", default="False")
inq_parser.add_argument('node', metavar='node', type=str)


args = inq_parser.parse_args()

NODEID = args.node
ORGFILTER = args.organization
SKIPORG = args.skiporg
NOTIFY_TOKEN = args.token
EVENT_THRESHOLD = args.threshold
REDIS_HOST=args.redis_host
REDIS_PORT=args.redis_port
EXTERNAL_REDIS_HOST=args.ext_redis_host
EXTERNAL_REDIS_PORT=args.ext_redis_port
CAMID=args.camid
COUNTER=args.counter
TRANSMIT=args.transmit


IS_S3=args.s3
CUSTOMER_BUCKET=args.bucket
MAX_CAMERAS=40


AWS_ACCESSKEY="AKIATVLJHPSRQZPX2QLY"
AWS_SECRETKEY="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"
TABLE_NAME="trackerdb"
NOTIFY_TABLE_NAME="notifydb"
BUCKET="inq-ai-tracking"
NOTIFY_BUCKET="inq-ai-notify"
REF_BUCKET="inq-ai-refbucket"
CONFIG_TABLE_NAME="nodeconfig"

API_BASE_URL="https://mwy1wltd6e.execute-api.af-south-1.amazonaws.com/prod/api-v1"
API_TOKEN="Token caa6f88508cbbc023223d7a814d0c3e44256a900"

TOKEN_LPR="6ebf94d717c9aea6187a0cc502bf013bb2ed5f8e"

FILEQ='fileq'
STREAMQ='streamq'
TRACKERQ='trackerq'
RULESQ='rulesq'
NOTIFYQ='notifyq'
CONFIGQ='configq'
FACEQ='faceq'
CAPQ='capq'
HEATMAP='heatmap'
FLOODLIGHT='floodlight'
DRIVERACTIVITY='driver_activity'
FACEMASK='facemask'
LPR="license_plate"
DEFAULT_CONF = 0.7
STREAMER_URL="http://edgeai-streamer-staging-856201964.af-south-1.elb.amazonaws.com"
STREAMER_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnbG9iYWxBY2Nlc3MiOnRydWUsImlhdCI6MTYwNDQ3NDA5Mn0.5GDxDybEBQVBSNgbRlNYygo7LRtjL0jqEdJBrXxuhRk"
CAM_RETRIES=10
DIFF_THRESHOLD=0.5
S3_BASE="https://inq-ai-notify.s3.af-south-1.amazonaws.com/"
QL_LIMIT_HIGH=10
QL_LIMIT_LOW=3
COMPARE_THRESHOLD=0.6



############## Input Variables #############

class DecimalEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return float(obj)
		return json.JSONEncoder.default(self, obj)


