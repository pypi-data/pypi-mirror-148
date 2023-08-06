import os
import uuid
import subprocess
import base64
import yaml
import boto3 

from halo import Halo
import emoji

from costack_cli.utils.aws_helpers import create_ecr_repository, get_boto3_session
from costack_cli.utils.requests import update_function_request
from costack_cli.config import load_project_config
from costack_cli.constants import BACKEND_ENDPOINT, CONFIG_PATH, BCOLORS
from costack_cli.config import init_config, get_user_login_info, save_project_config
from costack_cli.utils.requests import get_teams, create_function_request, get_authorization, create_api


def create_dynamo_db(team_id):
    # create dynamo for the current team 
    access_key, secret_key, _, region = get_authorization(team_id)
    dynamo_client = boto3.client('dynamodb', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    table_name = f"costack_context_{team_id}"
    response = dynamo_client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'function_id',
                'AttributeType': 'S'
            },
        ],
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'function_id',
                'KeyType': 'HASH'
            },
        ], 
        BillingMode='PAY_PER_REQUEST',
    )
    print(response)

