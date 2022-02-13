import sys
import time
from typing import Optional

from colorama import Fore
from datawrapper import Datawrapper
from pandas import DataFrame
from progressbar import *
from settings import DATAWRAPPER_FOLDER_NAME, DATAWRAPPER_TOKEN


dw = Datawrapper(access_token=DATAWRAPPER_TOKEN)
EXISTING_CHARTS = dw.get_charts(limit=9999)


def get_folder_id(folder_name: str) -> str:
    for folder in dw.get_folders()["data"][0]["folders"]:
        if folder["name"] == folder_name:
            return folder["id"]
    return ""


def chart_exists(title: str) -> Optional[dict]:
    for chart in EXISTING_CHARTS:
        if chart["title"] == title:
            return chart


def delete_all_charts_in_folder(folder: str):
    folder_id = get_folder_id(folder)
    for chart in EXISTING_CHARTS:
        if chart["folderId"] == folder_id:
            dw.delete_chart(chart["id"])


def generate_chart(
    data: dict, title: str, folder_id: Optional[str] = ""
) -> Optional[dict]:
    chart = chart_exists(title)
    if not chart:
        print(Fore.GREEN + f"Creating chart for {title}...")
        chart = dw.create_chart(
            title=title, chart_type="d3-bars", data=data, folder_id=folder_id
        )
        dw.update_metadata(chart["id"], {"visualize": {"sort-bars": True}})
        dw.publish_chart(chart["publicId"], display=False)
    else:
        time.sleep(0.02)
        print(
            Fore.YELLOW
            + f"Chart for {chart['title']} already exists with ID {chart['id']}"
        )
    return chart["publicId"]


def add_charts(items):
    FOLDER_ID = get_folder_id(DATAWRAPPER_FOLDER_NAME)
    USEFUL_COLUMNS = [
        "brexit party",
        "Tory",
        "BP+Tory",
        "Green",
        "Lab",
        "Lib Dem",
        "other",
        "plaid",
        "snp",
    ]
    titles = [item["Constituency name"].title() for item in items]
    constituencies_ids = [item["Constituency code"].title() for item in items]
    update = False

    if all(chart_exists(title) for title in titles):
        user_input = input(
            Fore.YELLOW
            + "\nAll charts exist in Datawrapper already. Do you want to update their data? (Y/n)"
        )
        update = user_input.lower() == "y"
        if not update:
            charts = [
                get_webflow_dict_from_chart(chart["publicId"], title, constituency_id)
                for title, constituency_id, chart in zip(
                    titles, constituencies_ids, EXISTING_CHARTS
                )
            ]
            return charts

    widgets = [
        FormatLabel(""),
        " ",
        Percentage(),
        " ",
        Bar("/"),
        " ",
        RotatingMarker(),
    ]
    progressbar = ProgressBar(widgets=widgets, maxval=len(items))
    progressbar.start()
    charts = []
    for i in range(len(items)):
        item = items[i]
        df = DataFrame.from_dict(
            {column: [column, item[column]] for column in USEFUL_COLUMNS},
            orient="index",
            columns=["party", "percentage"],
        )
        title = item["Constituency name"].title()
        constituency_id = item["Constituency code"].title()

        widgets[0] = FormatLabel(f"Creating chart for {title}...")
        progressbar.update(i)

        chart_id = generate_chart(df, title, FOLDER_ID)
    progressbar.finish()
    return charts


if __name__ == "__main__":
    globals()[sys.argv[1]](sys.argv[2])
