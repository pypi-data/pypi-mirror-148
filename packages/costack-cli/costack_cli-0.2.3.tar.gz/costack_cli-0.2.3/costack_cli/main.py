# https://hackersandslackers.com/python-poetry-package-manager/
import argparse
import os
import shutil
import pkgutil
import inquirer
import urllib.request

from costack_cli.build_project import create_function, update_function, deploy_from_config, initialize_project
from costack_cli.local_test import run_local_test, run_simple_local_test
from costack_cli.login import do_login_with_web_portal
from costack_cli.config import init_config, get_user_login_info, load_project_config
from costack_cli.utils.requests import get_teams, create_function_request, get_authorization
from costack_cli.utils.aws_helpers import create_ecr_repository, get_boto3_session
from costack_cli.local_test import run_simple_local_test
from costack_cli.constants import BCOLORS
from costack_cli.integrations import create_dynamo_db

def download_url(url, save_path):
    with urllib.request.urlopen(url) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())

def write_init_files():
    # download from s3 
    S3_PATH = "https://costack-public.s3.amazonaws.com/init_files.zip"
    download_url(S3_PATH, "init.zip")
    shutil.unpack_archive("init.zip", "./")
    os.remove("init.zip")
    # if not os.path.exists("model"):
    #     os.mkdir("model")
    if not os.path.exists("data"):
        os.mkdir("data")
    # this is the folder for test cases
    if not os.path.exists("test"):
        os.mkdir("test")
    

def init_dev_environment(skip_file_writes=False):
    team_list = get_teams()
    # print(team_list)
    team_name_list = [x["name"] for x in team_list]
    questions = [
        # inquirer.Text("function_name", "Name of the project"),
        # inquirer.Text("function_desc", "Description of the project"),
        # inquirer.Text("handler", message="Handler location that processes the request (<file name>.<method name>)", default="costack_main.handler"),
        inquirer.List('team_name',
            message="Select the team do you want to deploy functions to: ",
            choices=team_name_list
        )
    ]
    question_result = inquirer.prompt(questions)
    team_id = ""
    for team_record in team_list:
        if team_record["name"] == question_result["team_name"]:
            team_id = team_record["id"]
    
    # fetch the authorization 
    _, _, account_id, region = get_authorization(team_id)
    if not skip_file_writes:
        write_init_files()
    # initialize the image id for the functions 
    # TODO: check if the image url already existed 
    initialize_project(team_id, account_id, region)    
    print(f"{BCOLORS.OKGREEN}project initialization completed. Edit the costack.conf.yaml to build your project{BCOLORS.ENDC}")

def main(command_line=None):
    # base parser
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    login = subparser.add_parser('login')
    login.add_argument('-u', '--username', type=str, required=False)
    login.add_argument('-p', '--password', type=str, required=False)

    init = subparser.add_parser('init')
    init.add_argument('--skip-file-writes', action='store_true')
    # init.add_argument('-y', '--yaml', type=str, required=False)

    local_test = subparser.add_parser('test')
    local_test.add_argument('--function_name', type=str, default=False, required=True)
    local_test.add_argument('--input_json', type=str, default=False, required=True)
    # local_test.add_argument('--debug', type=str, default=False, required=False)

    deploy = subparser.add_parser('deploy')
    # deploy.add_argument('--debug', type=str, default=False, required=False)
    # deploy.add_argument('--update', action='store_true')
    # deploy.add_argument('--config', type=str, default=False, required=True)
    config = subparser.add_parser('config')
    # deploy.add_argument('--config', type=str, default=False, required=True)
    # show config 
    storage = subparser.add_parser('storage')
    # add storage to the workspace by creating a dynamo table for the workspace 
    storage.add_argument('--create', action='store_true')


    args = parser.parse_args()

    init_config()

    if args.command == 'login':
        do_login_with_web_portal()
    elif args.command == 'init':
        init_dev_environment(args.skip_file_writes)
    elif args.command == 'test':
        # run_local_test()
        run_simple_local_test(args.function_name, args.input_json)
    elif args.command == 'deploy':
        deploy_from_config()
    elif args.command == 'config':
        image_id, team_id, account_id, region = load_project_config()
        conf = {"image_id":image_id, "team_id":team_id}
        print(conf)
    elif args.command == 'storage':
        image_id, team_id, account_id, region = load_project_config()
        if args.create:
            # post dynamo create storage             
            create_dynamo_db(team_id)

if __name__ == '__main__':
    main()
