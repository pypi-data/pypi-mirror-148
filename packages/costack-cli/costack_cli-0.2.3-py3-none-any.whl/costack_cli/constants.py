from pathlib import Path
import os

CONFIG_HOME = os.path.join(Path.home(), '.costack')
CONFIG_PATH = "costack.conf.yaml"

USER_LOGIN_CONFIG = f"{CONFIG_HOME}/login.json"
USER_LOGIN_EMAIL_KEY = "user_email"
USER_ID_KEY = "user_id"
USER_JWT_TOKEN_KEY = "jwt_token"

FRONTEND_ENDPOINT = "https://beta.app.getcostack.com"
# FRONTEND_ENDPOINT = "http://localhost:3000"
BACKEND_ENDPOINT = "https://beta.backend.getcostack.com/api"
# BACKEND_ENDPOINT = "http://localhost:9100/api"
COSTACK_TOKEN_HEADER_KEY = 'entropy-auth'

PROJECT_CONFIG_PATH = "./.costack_conf.json"
FUNCTION_ID_KEY = "function_id"
TEAM_ID_KEY = "team_id"
ACCOUNT_ID_KEY = "account_id"
REGION_KEY = "region"

class BCOLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
