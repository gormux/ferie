from flask import Flask, render_template
from typing import List
from workalendar.europe import France, FranceAlsaceMoselle
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
app = Flask(__name__)
INDEX = "index.html"
TODAY = datetime.today().date()


def get_next_date(feries: List[datetime]) -> datetime:
    """Gets next holiday date

    :param feries: list of holidays
    :type feries: List[datetime]
    :return: next holiday
    :rtype: datetime
    """
    try:
        return next(_ for _ in feries if TODAY < _).strftime(r"%d %B")
    except StopIteration:
        return [_[0] for _ in France().holidays(TODAY.year + 1)][0]


def define_message(feries: List[datetime]) -> str:
    """Defines message for HTML page

    :param feries: list of holidays
    :type feries: List[datetime]
    :return: message
    :rtype: str
    """
    if TODAY in feries:
        return "Oui, profitez-en bien !"
    else:
        return f"Non, malheureusement, vivement le {get_next_date(feries)}"


@app.route("/")
def ferie():
    feries = [_[0] for _ in France().holidays(TODAY.year)]
    message = define_message(feries)
    return render_template(INDEX, message=message, alsace=False)


@app.route("/alsace-moselle")
def ferie_am():
    feries = [_[0] for _ in FranceAlsaceMoselle().holidays(TODAY.year)]
    message = define_message(feries)
    return render_template(INDEX, message=message, alsace=True)
