import sqlite3


from flask import Flask, render_template, request


DATABASE = "Database.db"


#testing changes


app = Flask(__name__)


def sqlsetup(sql):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


@app.route('/')

def homepage():
    return render_template("index.html", results=sqlsetup("SELECT * FROM Player;"))



@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/player')
def player():
    return render_template("player.html", results=sqlsetup("SELECT * FROM Player;"))

@app.route('/club')
def club():
    return render_template("club.html", results=sqlsetup("SELECT * FROM Club;"))

@app.route('/international')
def international():
    return render_template("international.html", results=sqlsetup("SELECT * FROM International;"))

@app.route('/award')
def award():
    return render_template("award.html", results=sqlsetup("SELECT * FROM Award;"))

@app.route('/club_awards')
def clubaward():
    return render_template("club_awards.html", results=sqlsetup("SELECT Award.award, Award.award_photo, Club.club, Club_award.count FROM Club_Award INNER JOIN Award ON Club_Award.award_id = Award.award_id INNER JOIN Club ON Club_Award.club_id = Club.club_id;"))


@app.route('/playeraward')
def playeraward():
    return render_template("playeraward.html", results=sqlsetup("SELECT Award.award,  Award.award_photo, Player.player, Player_Award.count FROM Player_Award INNER JOIN Award ON Player_Award.award_id = Award.award_id INNER JOIN Player ON Player_Award.player_id = Player.player_id;"))
   

if __name__ == "__main__":
    app.run(debug=True)