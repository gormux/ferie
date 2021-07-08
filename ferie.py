from flask import Flask
from typing import List
from workalendar.europe import France, FranceAlsaceMoselle
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
app = Flask(__name__)
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


@app.route("/")
def ferie():
    feries = [_[0] for _ in France().holidays(TODAY.year)]
    if TODAY in feries:
        return "Oui, profitez-en bien !"
    else:
        return f"Non, malheureusement, vivement le {get_next_date(feries)}"


@app.route("/alsace-moselle")
def ferie_am():
    feries = [_[0] for _ in FranceAlsaceMoselle().holidays(TODAY.year)]
    if TODAY in feries:
        return "Oui, profitez-en bien !"
    else:
        return f"Non, malheureusement, vivement le {get_next_date(feries)}"
