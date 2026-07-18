from flask import Flask, jsonify, render_template, request, redirect

app = Flask(__name__)

courses = []

@app.route("/")
def home():
    return render_template("index.html", courses=courses)

@app.route("/courseSelect")
def courseSelect():
    return render_template("courseSelect.html")

@app.route("/reserve.html")
def reserve():
    return render_template("reserve.html")

@app.route("/sedgely.html")
def sedgely():
    return render_template("sedgely.html")

@app.route("/playerSelect.html")
def playerSelect():
    return render_template("playerSelect.html")

currentRoundPlayers = []

@app.route("/startRound", methods=["POST"])
def startRound():
    global currentRoundPlayers

    data = request.get_json()
    currentRoundPlayers = data["players"]

    return "/round"


@app.route("/round")
def round():
    return render_template("round.html", players=currentRoundPlayers)



if __name__ == "__main__":
    app.run(debug=True)
