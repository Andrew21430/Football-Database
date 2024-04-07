import sqlite3


from flask import Flask, render_template, request


DATABASE = "Database.db"


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
    db.close()
    return render_template("index.html", results=results)


@app.route('/about')
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True)