import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

currentRoundPlayers = []


def get_db_connection():
    required_values = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    }

    if not all(required_values.values()):
        return None

    try:
        return psycopg2.connect(
            host=required_values["DB_HOST"],
            port=required_values["DB_PORT"],
            dbname=required_values["DB_NAME"],
            user=required_values["DB_USER"],
            password=required_values["DB_PASSWORD"],
        )
    except Exception as exc:
        print(f"Database connection failed: {exc}")
        return None


def fetch_courses():
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, location FROM courses ORDER BY name")
            return [
                {"id": row[0], "name": row[1], "location": row[2]}
                for row in cur.fetchall()
            ]
    finally:
        conn.close()


def fetch_players():
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM players ORDER BY name")
            return [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    finally:
        conn.close()


def create_round(player_names):
    conn = get_db_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO rounds (status) VALUES (%s) RETURNING id", ("active",))
            round_id = cur.fetchone()[0]

            for player_name in player_names:
                cur.execute("SELECT id FROM players WHERE name ILIKE %s", (player_name,))
                player_row = cur.fetchone()

                if player_row:
                    player_id = player_row[0]
                else:
                    cur.execute("INSERT INTO players (name) VALUES (%s) RETURNING id", (player_name,))
                    player_id = cur.fetchone()[0]

                cur.execute(
                    "INSERT INTO round_players (round_id, player_id, score) VALUES (%s, %s, %s)",
                    (round_id, player_id, 0),
                )

            return round_id
    finally:
        conn.close()


@app.route("/")
def home():
    return render_template("index.html", courses=fetch_courses())


@app.route("/courseSelect")
def courseSelect():
    return render_template("courseSelect.html", courses=fetch_courses())


@app.route("/reserve.html")
def reserve():
    return render_template("reserve.html")


@app.route("/sedgely.html")
def sedgely():
    return render_template("sedgely.html")


@app.route("/playerSelect.html")
def playerSelect():
    return render_template("playerSelect.html", players=fetch_players())


@app.route("/startRound", methods=["POST"])
def startRound():
    global currentRoundPlayers

    data = request.get_json(silent=True) or {}
    currentRoundPlayers = data.get("players", [])
    create_round(currentRoundPlayers)

    return "/round"


@app.route("/round")
def round():
    return render_template("round.html", players=currentRoundPlayers)


if __name__ == "__main__":
    app.run(debug=True)
