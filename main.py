import os
import sys

from colorama import Fore

from services.datawrapper_service import add_charts
from services.google_service import get_sheet_rows
from services.webflow_service import update_collection

sheet_rows = get_sheet_rows()

# charts = add_charts(sheet_rows)
update_collection(sheet_rows)

print(Fore.CYAN + "\nFinished running the script\n")
