import time
from os import environ

from colorama import Fore
from dotenv import load_dotenv

load_dotenv("config.yaml")


def quit_script(missing_keys):
    for key in missing_keys:
        print(
            Fore.RED
            + f"Missing {' '.join(key.split('_')).title()}, please add it or the script can't run"
        )
    time.sleep(2)
    quit()


missing_variables = []

DATAWRAPPER_FOLDER_NAME = environ.get("DATAWRAPPER_TOKEN", None)
DATAWRAPPER_TOKEN = environ.get("DATAWRAPPER_TOKEN", None)
if not DATAWRAPPER_TOKEN:
    missing_variables.append("DATAWRAPPER_TOKEN")
WEBFLOW_COLLECTION_NAME = environ.get("WEBFLOW_COLLECTION_NAME", None)
if not WEBFLOW_COLLECTION_NAME:
    missing_variables.append("WEBFLOW_COLLECTION_NAME")
WEBFLOW_SITE_NAME = environ.get("WEBFLOW_SITE_NAME", None)
if not WEBFLOW_SITE_NAME:
    missing_variables.append("WEBFLOW_SITE_NAME")
WEBFLOW_TOKEN = environ.get("WEBFLOW_TOKEN", None)
if not WEBFLOW_TOKEN:
    missing_variables.append("WEBFLOW_TOKEN")
GOOGLE_SHEET_ID = environ.get("GOOGLE_SHEET_ID", None)
if not GOOGLE_SHEET_ID:
    missing_variables.append("GOOGLE_SHEET_ID")

if missing_variables:
    quit_script(missing_variables)
