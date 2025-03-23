from zetros import ZetrosInterface
from flask import Flask

app = Flask(__name__)
i = ZetrosInterface()

back = "<html><head><script>history.back()</script></head></html>"

@app.route('/')
def main():
    return ("<a href=\"/left\">Left</a> | "
            "<a href=\"/forward\">Forward</a> |"
            "<a href=\"/right\">Right</a> |"
            "<a href=\"/backward\">Backward</a> ")

@app.route("/forward")
def forward():
    i.user_drive("forward")
    return back

@app.route("/left")
def left():
    i.user_drive("left")
    return back

@app.route("/right")
def right():
    i.user_drive("right")
    return back

@app.route("/backward")
def backward():
    i.user_drive("backward")
    return back

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)