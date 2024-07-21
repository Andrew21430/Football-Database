import sqlite3


from flask import Flask, render_template, request


DATABASE = "Database.db"


# testing changes


app = Flask(__name__)


def sqlsetup(sql):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor() 
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def spliter(data):
    splits = data.split("&")
    for i in range(0, len(splits)):
        splits[i] = filter(str.isdecimal, str(splits[i]))
        splits[i] = "".join(splits[i])
    return splits


@app.route('/')
def homepage():
    return render_template("index.html", results=sqlsetup("SELECT * FROM Player;"))


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/player', methods=['GET', 'POST'])
def player():
    player = str(request.get_data('player'))
    if request.method == 'POST':
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        results = []
        splitplayer = spliter(player)
        for i in range(0, len(spliter(player))):
            cursor.execute("SELECT Player.player, Club.club, Player.total_apperances, International.country, Player.photo, Player.player_id FROM Player INNER JOIN Club ON Player.club_id = Club.club_id INNER JOIN International ON Player.international_id = International.international_id WHERE Player.player_id =?", (splitplayer[i],))
            add = cursor.fetchall()
            results.extend(add)
        return render_template("player.html", results=results, fulllist=sqlsetup("SELECT Player.player, Club.club, Player.total_apperances, International.country, Player.photo, Player.player_id FROM Player INNER JOIN Club ON Player.club_id = Club.club_id INNER JOIN International ON Player.international_id = International.international_id;"), size=len(results))
    else:    
        return render_template("player.html", results=sqlsetup("SELECT Player.player, Club.club, Player.total_apperances, International.country, Player.photo, Player.player_id FROM Player INNER JOIN Club ON Player.club_id = Club.club_id INNER JOIN International ON Player.international_id = International.international_id;"), fulllist=sqlsetup("SELECT Player.player, Club.club, Player.total_apperances, International.country, Player.photo FROM Player INNER JOIN Club ON Player.club_id = Club.club_id INNER JOIN International ON Player.international_id = International.international_id;"))


@app.route('/club', methods=['GET', 'POST'])
def club():
    club = str(request.get_data('club'))
    if request.method == 'POST':
        print(club)
        splitclub = spliter(club)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        results = []
        for i in range(0, len(splitclub)):
            cursor.execute("SELECT Club.club_id, Club.club, Club.description, League.league, Club.emblem FROM Club INNER JOIN League ON Club.league_id = League.League_id WHERE Club.club_id =?", (splitclub[i],))
            add = cursor.fetchall()
            results.extend(add)
        return render_template("club.html", results=results, fulllist=sqlsetup("SELECT Club.club_id, Club.club, Club.description, League.league, Club.emblem FROM Club INNER JOIN League ON Club.league_id = League.League_id ORDER BY Club.club ASC;"), size=len(results))
    else: 
        return render_template("club.html", results=sqlsetup("SELECT Club.club_id, Club.club, Club.description, League.league, Club.emblem FROM Club INNER JOIN League ON Club.league_id = League.League_id ORDER BY Club.club ASC;"), fulllist=sqlsetup("SELECT Club.club_id, Club.club, Club.description, League.league, Club.emblem FROM Club INNER JOIN League ON Club.league_id = League.League_id ORDER BY Club.club ASC;"))


@app.route('/international', methods=['GET', 'POST'])
def international():
    international = str(request.get_data('international'))
    if request.method == 'POST':
        print(international)
        splitinternational = spliter(international)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        results = []
        for i in range(0, len(splitinternational)):
            cursor.execute("SELECT * FROM International WHERE international_id = ?", (splitinternational[i],))
            add = cursor.fetchall()
            results.extend(add)
        return render_template("international.html", results=results, fulllist=sqlsetup("SELECT * FROM International ORDER BY country ASC;"), size=len(results))
    else: 
        return render_template("international.html", results=sqlsetup("SELECT * FROM International ORDER BY country ASC;"), fulllist=sqlsetup("SELECT * FROM International ORDER BY country ASC;"))

# @app.route('/award')
# def award():
#   return render_template("award.html", results=sqlsetup("SELECT * FROM Award;"))


@app.route('/club_awards')
def clubaward():
    seen = ['test']
    return render_template("club_awards.html", seen=seen, results=sqlsetup("SELECT Award.award, Award.award_photo, Club.club, Club_award.count FROM Club_Award INNER JOIN Award ON Club_Award.award_id = Award.award_id INNER JOIN Club ON Club_Award.club_id = Club.club_id ORDER BY Club_Award.award_id ASC, Club_Award.count DESC, Club.club ASC;"))


@app.route('/playeraward')
def playeraward():
    seen = ['test']
    return render_template("playeraward.html", seen=seen, results=sqlsetup("SELECT Award.award,  Award.award_photo, Player.player, Player_Award.count FROM Player_Award INNER JOIN Award ON Player_Award.award_id = Award.award_id INNER JOIN Player ON Player_Award.player_id = Player.player_id ORDER BY Player_Award.award_id ASC, Player_Award.count DESC, Player.player ASC;"))
   

@app.route('/league')
def league():
    seen = ['test']
    return render_template("league.html", seen=seen, results=sqlsetup("SELECT * From League;"))


@app.route('/triangle/up/right/<int:size>')
def triangle(size):
    row = []
    for i in range(0, size+1):
        spaces = size - i
        line = ' '*spaces + '*'*i
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


@app.route('/triangle/up/left/<int:size>')
def triangle_up_left(size):
    row = []
    for i in range(0, size+1):
        spaces = size - i
        line = '*'*i + ' '*spaces
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


@app.route('/triangle/down/right/<int:size>')
def triangle_down_right(size):
    row = []
    for i in range(0, size+1):
        spaces = size - i
        line = ' '*i + '*'*spaces
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


@app.route('/triangle/down/left/<int:size>')
def triangle_down_left(size):
    row = []
    for i in range(0, size+1):
        spaces = size - i
        line = '*'*spaces + ' '*i
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


@app.route('/diamond/hollow/<int:size>')
def Hollow_diamond(size):
    row = []
    increase = 0
    for i in range(1, size+1):
        increase = increase - i
        spaces = size - i
        if i == 1:
            row.append(' '*spaces + '*' + ' '*spaces)
        else:
            line = ' '*spaces + '*' + ' '*(((i-1)*2)-1) + '*' + ' '*spaces
            row.append(line)
            if i == size:
                for x in range(1, i):
                    spaces = size - (i-x)
                    if x == i-1:
                        row.append(' '*spaces + '*')
                    else:
                        line = ' '*spaces + '*' + ' '*((((i-x)-1)*2)-1) + '*'
                        row.append(line)
    length = len(row)
    
    return render_template('diamond.html', row=row, length=length,)


@app.route('/award', methods=['GET', 'POST'])
def award():
    trophy = str(request.get_data('trophies'))
    print(trophy)
    if request.method == 'POST':
        print(trophy)
        splittrophy = spliter(trophy)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        results = []
        for i in range(0, len(splittrophy)):
            cursor.execute("SELECT * FROM Award WHERE award_id =?", (splittrophy[i],))
            add = cursor.fetchall()
            results.extend(add)
        return render_template("award.html", results=results, fulllist=sqlsetup("SELECT * FROM Award"), size=len(results))
    else:    
        return render_template("award.html", results=sqlsetup("SELECT * FROM Award"), fulllist=sqlsetup("SELECT * FROM Award"))


@app.route('/playerclubs')
def playerclubs():
    seen = ['test']
    return render_template("playerclubs.html", seen=seen, results=sqlsetup("SELECT Club.club, Club.emblem, Player.player, Player.photo, past_player_club.apperances From past_player_club INNER JOIN Club on past_player_club.club_id = Club.club_id INNER JOIN Player ON past_player_club.player_id = Player.player_id ORDER BY Club.club ASC;"))    


@app.route('/internationalawards')
def internationalawards():
    seen = ['test']
    return render_template("internationalaward.html", seen=seen, results=sqlsetup("SELECT Award.award, Award.award_photo, International.country, International_Award.count FROM International_Award INNER JOIN Award on International_Award.award_id = Award.award_id INNER JOIN International ON International_Award.international_id = International.International_id ORDER BY International_award.award_id ASC, International_Award.count DESC;"))


@app.route('/internationalapperances')
def internationalapperances():
    seen = ['test']
    return render_template("internationalapperances.html", seen=seen, results=sqlsetup("SELECT International.country, International.flag, Player.player, Player.photo, International_apperances.apperances FROM International_apperances INNER JOIN Player on International_apperances.player_id = Player.player_id INNER JOIN International ON International_apperances.international_id = International.International_id ORDER BY International.country ASC, International_apperances.apperances DESC;"))


if __name__ == "__main__":
    app.run(debug=True)
    