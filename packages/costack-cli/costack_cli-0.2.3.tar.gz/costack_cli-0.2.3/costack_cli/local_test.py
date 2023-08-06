# https://hackersandslackers.com/python-poetry-package-manager/
import argparse
import sys
import os
import shutil
import json
import requests
import webbrowser
import subprocess
import boto3
import yaml
from pathlib import Path
from costack_cli.constants import CONFIG_PATH, BCOLORS

def run_local_test():
    # post to the url
    if not os.path.exists(".costack_conf"):
        print("no project information found, initialize first")
        return

    with open(f".costack_conf", "r") as f:
        conf = json.load(f)
    parameters = conf['function_detail']['parameters']
    function_id = conf['function_id']
    # enter the parameters and run the test
    # enter the values for the parameters and use local environment to run the test

    test_image_tag = f"{function_id}:latest"
    print(f"test image tag is {test_image_tag}")

    DOCKER_BUILD_CMD = f"docker build -t {test_image_tag} ."
    DOCKER_RUN_CMD = f"docker run -d -p 9000:8080 {test_image_tag}"
    print(DOCKER_BUILD_CMD)
    subprocess.run(DOCKER_BUILD_CMD, shell=True, check=True)
    print("done building image")
    print("build docker...")
    print(DOCKER_RUN_CMD)
    subprocess.run(DOCKER_RUN_CMD, shell=True, check=True)

    param_json = {}
    for param in parameters:
        # enter the parameters
        param_json[param] = input(f"enter value for {param}: ")
    try:
        subprocess.run(f"curl -XPOST \"http://localhost:9000/2015-03-31/functions/function/invocations\" -d '{json.dumps(param_json)}'", shell=True, check=True)
    except Exception as e:
        # clean the port
        print(f"encountered error {e}")

    print("\n cleaning up local running container")
    STOP_DOCKER_COMMAND = f"docker stop $(docker ps -q --filter ancestor={test_image_tag})"
    subprocess.run(STOP_DOCKER_COMMAND, shell=True, check=True)


def run_simple_local_test(funciton_name, input_path):
    #load the config 
    if not os.path.exists(input_path):
        # input does not exists
        print(f"{BCOLORS.FAIL}input path {input_path} does not exist{BCOLORS.ENDC}")
        exit()
    with open(CONFIG_PATH, 'r') as stream:
        deploy_config = yaml.safe_load(stream)
    # check if the function exists 
    function_item = [item for item in deploy_config['functions'] if item['name']==funciton_name] 
    if not function_item:
        print(f"{BCOLORS.FAIL} function {funciton_name} does not exist in config{BCOLORS.ENDC}")
        exit()
    function = function_item[0]
    print(f"{BCOLORS.WARNING}WARNING: make sure you have sourced the virtual environment to run the test. if not run:\npython3.8 -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt {BCOLORS.ENDC}")
    print("-"*20)
    name, function_id, handler, description = function['name'], function['id'], function['handler'], function['description']
    # just need to get the handler 
    # get the handler path 
    handler_path, function_name = ".".join(handler.split(".")[:-1]), handler.split(".")[-1]
    test_script = f"""
import sys
import json 
from {handler_path} import {function_name}
# json_path = sys.argv[1]
with open('{input_path}', 'r') as f:
    event = json.loads(f.read())
print(f'{BCOLORS.OKCYAN}test input is: {BCOLORS.ENDC}')
print(event)
context = None 
result = {function_name}(event, context)
print(f'{BCOLORS.OKGREEN}test result is: {BCOLORS.ENDC}')
print(result)
"""
    
    os.system(f"python3.8 -c \"{test_script}\" ")

