from flask import Flask
from workalendar.europe import France
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
app = Flask(__name__)


@app.route("/")
def ferie():
    today = datetime.today().date()
    feries = [_[0] for _ in France().holidays(today.year)]
    try:
        next_date = next(_ for _ in feries if today < _).strftime(r"%d %B")
    except StopIteration:
        next_date = [_[0] for _ in France().holidays(today.year + 1)][0]
    if today in feries:
        return "Oui, profitez-en bien !"
    else:
        return f"Non, malheureusement, vivement le {next_date}"
