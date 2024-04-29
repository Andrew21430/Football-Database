import sqlite3


from flask import Flask, render_template, request


DATABASE = "Database.db"


#testing changes


app = Flask(__name__)



@app.route('/')

def homepage():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    # sql statement
    sql = "SELECT * FROM Player;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("index.html", results=results)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/player')
def player():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    # sql statement
    sql = "SELECT * FROM Player;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("player.html", results=results)

@app.route('/club')
def club():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    # sql statement
    sql = "SELECT * FROM Club;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("club.html", results=results)

@app.route('/international')
def international():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    # sql statement
    sql = "SELECT * FROM International;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("international.html", results=results)

@app.route('/award')
def award():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    # sql statement
    sql = "SELECT * FROM Award;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("award.html", results=results)

@app.route('/club_awards')
def clubaward():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    # sql statement
    sql = "SELECT Award.award, Club.club, Club_award.count FROM Club_Award INNER JOIN Award ON Club_Award.award_id = Award.award_id INNER JOIN Club ON Club_Award.club_id = Club.club_id;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("club_awards.html", results=results)



if __name__ == "__main__":
    app.run(debug=True)