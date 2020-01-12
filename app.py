from flask import Flask, request, abort, request
from subprocess import run, Popen
import hmac
import hashlib
from os import environ
from os.path import isdir, isfile
from os import mkdir
from sqlite3 import connect

if not isdir("/TelegramEDT/.git"):
    run(["git", "clone", "https://github.com/flifloo/TelegramEDT.git", "/TelegramEDT"])
if (not isdir("/TelegramEDT/alembic")) and isfile("/TelegramEDT/edt.db"):
    c = connect("/TelegramEDT/edt.db")
    c.execute("delete from alembic_version;")
    c.commit()

app = Flask(__name__)
webhook_secret = environ.get("webhook_secret")
bot = Popen(["python3", "main.py"], cwd="/TelegramEDT/")

@app.route("/git", methods=["POST"])
def git():
    if not "X-Hub-Signature" in request.headers:
        abort(400)

    request.get_data()
    signature = request.headers['X-Hub-Signature']
    payload = request.data

    secret = webhook_secret.encode()
    hmac_gen = hmac.new(secret, payload, hashlib.sha1)
    digest = "sha1=" + hmac_gen.hexdigest()


    if signature != digest:
        abort(400)
    global bot
    bot.kill()

    run(["git", "pull"], cwd="/TelegramEDT/")
    run(["bash", "./update.sh"], cwd="/TelegramEDT/")
    bot = Popen(["python3", "main.py"], cwd="/TelegramEDT/")
    return "Ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0")

