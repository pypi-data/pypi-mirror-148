import os
import uuid
import subprocess
import base64
import yaml

from halo import Halo
import emoji

from costack_cli.utils.aws_helpers import create_ecr_repository, get_boto3_session
from costack_cli.utils.requests import update_function_request
from costack_cli.config import load_project_config
from costack_cli.constants import BACKEND_ENDPOINT, CONFIG_PATH, BCOLORS
from costack_cli.config import init_config, get_user_login_info, save_project_config
from costack_cli.utils.requests import get_teams, create_function_request, get_authorization, create_api

spinner = Halo(text='Loading', spinner='dots')

def get_image_uri(account_id, region, repository_name):
    return f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}"

def tag_latest_uri(image_uri):
    return f"{image_uri}:latest"

def get_registry_access_token(ecr_client, repo_id):
    response = ecr_client.get_authorization_token(
        registryIds=[
            repo_id,
        ]
    )
    return base64.b64decode(response['authorizationData'][0]['authorizationToken']).decode('utf-8')[4:]

def build_and_push_image(ecr_access_token, function_id, latest_image_uri, account_id, region):
    # invoke docker to build image
    subprocess.run(
        [f"docker login --username AWS --password {ecr_access_token} {account_id}.dkr.ecr.{region}.amazonaws.com"], shell=True)
    subprocess.run([f"docker build --file .Dockerfile -t {function_id} ."], shell=True)
    subprocess.run(
        [f"docker tag {function_id}:latest {latest_image_uri}"], shell=True)
    subprocess.run([f"docker push {latest_image_uri}"], shell=True)

def deploy_from_config():
    _, team_id, _, _ = load_project_config()
    image_id, team_id, account_id, region = load_project_config()
    user_id, _ = get_user_login_info()
    # we only need the team id 
    # use yaml to load the config path 
    # Read YAML file
    with open(CONFIG_PATH, 'r') as stream:
        deploy_config = yaml.safe_load(stream)
    # TODO: validate deployment config yam; file 
    # print("read yaml file ", deploy_config)
    # build the image 
    print(f"{BCOLORS.WARNING}start building image, make sure your docker client is running{BCOLORS.ENDC}")
    # build a consistent image uri first for the function 
    image_uri = _build_image()
    # image_uri = "372183484622.dkr.ecr.us-east-1.amazonaws.com/e818f265-c755-473d-b902-83d2660d92a0"
    # TODO: Add debug prints 
    # print(f"building image complete, image uri is {image_uri}")
    
    print("-"*20)
    print("deploying costack functions...")
    function_name_id_mapping = {}
    for function in deploy_config['functions']: 
        # get the function id 
        name, function_id, handler, description = function['name'], function['id'], function['handler'], function['description']
        # TODO: validate handler path is correct 
        # update the function if funciton not exists, create the function 
        if function_id is None:
            # create function 
            print(f"{BCOLORS.OKBLUE}function id not found for function {name}, creating new function{BCOLORS.ENDC}")
            # spinner 
            spinner.start()
            function_id = str(uuid.uuid4())
            response = create_function(function_id, team_id, name, description, image_uri, handler)
            # spinner 
            spinner.stop()
            print(response.text)
            # update the function id 
            function['id'] = function_id
        else:
            print(f"{BCOLORS.OKBLUE}found existing id for function {name}, updating function...{BCOLORS.ENDC}")
            # handler corresponds to the docker command 
            # spinner 
            spinner.start()
            response = update_function_request(team_id, function_id, image_uri, handler)
            spinner.stop()
            print(response.text)
        function_name_id_mapping[name] = function_id

    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(deploy_config, file)
    print("-"*20)
    print("deploying costack apis...")
    
    apis = deploy_config.get('apis', [])
    if not apis:
        print("no api found, skip deployment") 
        return 
    for api in apis: 
        function_name, http_method, route_path = api['function_name'], api['http_method'], api['path']
        function_id = function_name_id_mapping[function_name]
        # call deploy api  
        response = create_api(user_id, team_id, function_id, route_path, http_method)
        print(f"[NEW API RESOURCE] {http_method}, {route_path}, {function_name}...")
        if response.status_code == 201:
            print(f"create api response ", response.text)
        else:
            print(f"{BCOLORS.FAIL}api creation failed{BCOLORS.ENDC}: {response.text}")
            print(response.text)

    print(emoji.emojize(f":unicorn::unicorn::unicorn:{BCOLORS.OKGREEN}deployment successful, update config file{BCOLORS.ENDC}"))
    # print("Model successfully updated!")

def update_function():
    function_id, team_id, _, _ = load_project_config()
    image_uri = _build_image()
    update_function_request(team_id, function_id, image_uri)
    print("Model successfully updated!")

def initialize_project(team_id, account_id, region): 
    user_id, _ = get_user_login_info()
    # _, _, account_id, region = get_authorization(team_id)
    # function_id = str(uuid.uuid4())
    image_id = str(uuid.uuid4())
    save_project_config(image_id, team_id, account_id, region)
    # create the ecr 
    boto3_session = get_boto3_session(team_id)
    ecr_client = boto3_session.client('ecr')
    create_ecr_repository(ecr_client, image_id)

def create_function(function_id, team_id, function_name, function_desc, image_uri, docker_command):
    user_id, _ = get_user_login_info()
    _, _, account_id, region = get_authorization(team_id)
    # function_id = str(uuid.uuid4())
    image_id = str(uuid.uuid4())
    # save_project_config(image_id, team_id, account_id, region)
    # boto3_session = get_boto3_session(team_id)
    # ecr_client = boto3_session.client('ecr')
    # create_ecr_repository(ecr_client, image_id)
    # image_uri = _build_image()
    return create_function_request(
        function_id,
        user_id,
        team_id, 
        function_name,
        function_desc, 
        image_uri, 
        docker_command)

def _build_image():
    # validate_project_folder()
    image_id, team_id, account_id, region = load_project_config()
    boto3_session = get_boto3_session(team_id)
    ecr_client = boto3_session.client('ecr')

    latest_image_uri = tag_latest_uri(get_image_uri(account_id, region, image_id))
    access_token = get_registry_access_token(ecr_client, account_id)
    build_and_push_image(access_token, image_id,
                         latest_image_uri, account_id, region)
    return latest_image_uri


