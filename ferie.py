from flask import Flask, render_template
from typing import List
from datetime import datetime
import locale
import importlib

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
app = Flask(__name__)
INDEX = "index.html"
TODAY = datetime.today().date()
ZONES = ["africa", "america", "asia", "europe", "oceania", "usa"]


def get_cal(zone=None):
    zones = {}
    continents = {_: importlib.import_module(f"workalendar.{_}") for _ in ZONES}
    for _, v in continents.items():
        for item in dir(v):
            truc = getattr(v, item)
            if isinstance(truc, type):
                zones[item] = truc
    if zone:
        return zones[zone]
    return zones.keys()


def get_next_date(cal, feries: List[datetime]) -> datetime:
    """Gets next holiday date

    :param feries: list of holidays
    :type feries: List[datetime]
    :return: next holiday
    :rtype: datetime
    """
    try:
        return next(_ for _ in feries if TODAY < _).strftime(r"%d %B")
    except StopIteration:
        return [_[0] for _ in cal().holidays(TODAY.year + 1)][0]


def define_message(cal, feries: List[datetime]) -> str:
    """Defines message for HTML page

    :param feries: list of holidays
    :type feries: List[datetime]
    :return: message
    :rtype: str
    """
    if TODAY in feries:
        return "Oui, profitez-en bien !"
    else:
        return f"Non, malheureusement, vivement le {get_next_date(cal, feries)}"


@app.route("/")
def main():
    return render_template("list.html", zones=get_cal())


@app.route("/<zone>")
def ferie(zone: str):
    cal = get_cal(zone)
    feries = [_[0] for _ in cal().holidays(TODAY.year)]
    message = define_message(cal, feries)
    return render_template(INDEX, message=message)
