import sqlite3


from flask import Flask, render_template, request


DATABASE = "Database.db"


#testing changes


app = Flask(__name__)


'''SQL Functions'''


'''Printing'''


def print_players():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    # sql statement
    sql = "SELECT * FROM Player;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #print format
    print(f"{'id':<10} {'player':<30} {'club id':<10} {'apperances':<15} {'age':<5} {'club count':<15} {'international id'}")
    for player in results:
        #printing out the data
        print(f"{player[0]: <10} {player[1]:<30} {player[2]:<10} {player[3]:<15} {player[4]:<5} {player[5]:<15} {player[6]} ")
    db.close()


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



if __name__ == "__main__":
    app.run(debug=True)