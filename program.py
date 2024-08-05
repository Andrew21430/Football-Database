# Flask and sql setup

import sqlite3


from flask import Flask, render_template, request


DATABASE = "Database.db"


# testing changes

# app creation
app = Flask(__name__)


# function for sql querrys to reduce copying
def sqlsetup(sql):
    # connecting to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    # excute sql querry
    cursor.execute(sql)
    # return the results
    results = cursor.fetchall()
    return results


# Function used to split data received from the form submission
def spliter(data):
    # inputs are slipt on the & and this what is used for forms to split
    # multiple responses
    splits = data.split("&")
    # this code lops through the new vaules and seprates them into decimal
    # values so they can be read and utilised in the databse
    for i in range(0, len(splits)):
        splits[i] = filter(str.isdecimal, str(splits[i]))
        splits[i] = "".join(splits[i])
    return splits


'''Start of webpages '''


@app.route('/')
def homepage():
    # variable declaration for each sql querry values
    # that get used for each page
    query = "SELECT * FROM Player;"
    return render_template("index.html", results=sqlsetup(query))


@app.route('/about')
def about():
    return render_template("about.html")


# the players page as a submition for so we need to check and see if any
# data has been sent
@app.route('/player', methods=['GET', 'POST'])
def player():
    # resqut the data reseived rom the form eg player=2
    player = str(request.get_data('player'))
    # delcaring all sql statments used
    query = 'SELECT Player.player, Club.club, Player.total_apperances, International.country, Player.photo, Player.player_id FROM Player INNER JOIN Club ON Player.club_id = Club.club_id INNER JOIN International ON Player.international_id = International.international_id'
    where = query
    where += ' WHERE Player.player_id =?'
    order = query
    order += ' ORDER BY Player.player ASC'
    # if we do reseve a value from the form
    if request.method == 'POST':
        # database connection
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        # creates results as a list so we can loop through our results and
        # then add them into results
        results = []
        # runs the splitter function to seperate all our values to just numbers
        splitplayer = spliter(player)
        # loop thourgh all the results we got
        for i in range(0, len(spliter(player))):
            cursor.execute(where, (splitplayer[i],))
            # ad each result to results as a new item in the list
            add = cursor.fetchall()
            results.extend(add)
        # fulllist is the full sql database for use in the selection boxes
        return render_template(
            "player.html", results=results, fulllist=sqlsetup(order), size=len(results))
    else:
        return render_template("player.html", results=sqlsetup(order), fulllist=sqlsetup(order))


# Club page re-uses the formating from the player table
@app.route('/club', methods=['GET', 'POST'])
def club():
    club = str(request.get_data('club'))
    query = 'SELECT Club.club_id, Club.club, Club.description, League.league, Club.emblem FROM Club INNER JOIN League ON Club.league_id = League.League_id'
    where = query
    where += ' WHERE Club.club_id =?'
    order = query
    order += ' ORDER BY Club.club ASC'
    if request.method == 'POST':
        splitclub = spliter(club)
        print(splitclub)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        results = []
        for i in range(0, len(splitclub)):
            cursor.execute(where, (splitclub[i],))
            add = cursor.fetchall()
            results.extend(add)
        return render_template("club.html", results=results, fulllist=sqlsetup(order), size=len(results))
    else:
        return render_template("club.html", results=sqlsetup(order), fulllist=sqlsetup(order))


# Same with International
@app.route('/international', methods=['GET', 'POST'])
def international():
    international = str(request.get_data('international'))
    query = 'SELECT * FROM International'
    where = query
    where += ' WHERE international_id = ?'
    order = query
    order += ' ORDER BY country ASC'
    if request.method == 'POST':
        splitinternational = spliter(international)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        results = []
        for i in range(0, len(splitinternational)):
            cursor.execute(where, (splitinternational[i],))
            add = cursor.fetchall()
            results.extend(add)
        return render_template("international.html", results=results, fulllist=sqlsetup(order), size=len(results))
    else:
        return render_template("international.html", results=sqlsetup(order), fulllist=sqlsetup(order))


# listing out the amount of times an award has been won by clubs
@app.route('/club_awards')
def clubaward():
    # seen is used to stop the repeation of list out award names with the
    # peroius award was the same i.e this stiops duplicates
    seen = ['no']
    # long sql querry as a bridge table is used along with
    # multiple forms of ordering
    query = "SELECT Award.award, Award.award_photo, Club.club, Club_award.count FROM Club_Award INNER JOIN Award ON Club_Award.award_id = Award.award_id INNER JOIN Club ON Club_Award.club_id = Club.club_id ORDER BY Club_Award.award_id ASC, Club_Award.count DESC, Club.club ASC;"
    return render_template("club_awards.html", seen=seen, results=sqlsetup(query))


# listing out the amount of times each awards has been won by diffrent players
# which re-uses the code from the previous bridge table
@app.route('/playeraward')
def playeraward():
    seen = ['no']
    query = "SELECT Award.award, Award.award_photo, Player.player, Player_Award.count FROM Player_Award INNER JOIN Award ON Player_Award.award_id = Award.award_id INNER JOIN Player ON Player_Award.player_id = Player.player_id ORDER BY Player_Award.award_id ASC, Player_Award.count DESC, Player.player ASC;"
    return render_template("playeraward.html", seen=seen, results=sqlsetup(query))


# listing out the leagues
@app.route('/league')
def league():
    return render_template("league.html", results=sqlsetup("""
        SELECT * From League;"""))


# Coding challgenge to create diffrent triangles that can have their size and
# dirrection altered by different url
@app.route('/triangle/up/right/<int:size>')
def triangle(size):
    # create a item in a list for each row that can be looped through to list
    # the triangle
    row = []
    for i in range(0, size+1):
        # creates the spaces needed in front of the triangle so it slopes
        # towards the top right
        spaces = size - i
        # creates the line by multipling the amout of * and spaces needed
        line = ' '*spaces + '*'*i
        # add each line to the list to be run thourgh later
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


# slopes up to the top left of the page
@app.route('/triangle/up/left/<int:size>')
def triangle_up_left(size):
    row = []
    for i in range(0, size+1):
        spaces = size - i
        line = '*'*i + ' '*spaces
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


# triangle that slopes down to the bottom right
@app.route('/triangle/down/right/<int:size>')
def triangle_down_right(size):
    row = []
    for i in range(0, size+1):
        spaces = size - i
        line = ' '*i + '*'*spaces
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


# triangle that slopes down to the bottom left
@app.route('/triangle/down/left/<int:size>')
def triangle_down_left(size):
    row = []
    for i in range(0, size+1):
        spaces = size - i
        line = '*'*spaces + ' '*i
        row.append(line)
    return render_template('triangle.html', row=row, size=size)


# Coding challenge to create a diamond that is hollow and can have its size
# altered by changing the url
@app.route('/diamond/hollow/<int:size>')
def Hollow_diamond(size):
    row = []
    for i in range(1, size+1):
        spaces = size - i
        # if i is one then we need to have only a single chracter which would
        # not work with the standard code for each line as two * are used
        if i == 1:
            row.append(' '*spaces + '*' + ' '*spaces)
        else:
            # add the next two * spaced out
            line = ' '*spaces + '*' + ' '*(((i-1)*2)-1) + '*' + ' '*spaces
            row.append(line)
            # check to see when we get to half way in the diamond as the
            # code is required to change
            if i == size:
                # re uses the same steps as before how ever the spaces
                # increase instead of decreasing
                for x in range(1, i):
                    spaces = size - (i-x)
                    if x == i-1:
                        row.append(' '*spaces + '*')
                    else:
                        line = ' '*spaces + '*' + ' '*((((i-x)-1)*2)-1) + '*'
                        row.append(line)
    # used to have the size of the diamond so the pages lists out the correct
    # amount of lines beacus len()
    length = len(row)
    return render_template('diamond.html', row=row, length=length,)


# listing out awards seperated by country and international
@app.route('/award', methods=['GET', 'POST'])
def award():
    trophy = str(request.get_data('trophies'))
    query = "SELECT * FROM Award"
    where = query
    where += " WHERE award_id =?"
    # full list of data
    data = sqlsetup(query)
    if request.method == 'POST':
        splittrophy = spliter(trophy)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        results = []
        for i in range(0, len(splittrophy)):
            cursor.execute(where, (splittrophy[i],))
            add = cursor.fetchall()
            results.extend(add)
        return render_template("""award.html
        """, results=results, fulllist=data, size=len(results))
    else:
        return render_template("award.html", results=data, fulllist=data)


@app.route('/playerclubs')
def playerclubs():
    seen = ['test']
    return render_template("playerclubs.html", seen=seen, results=sqlsetup(
        """SELECT Club.club, Club.emblem, Player.player, Player.photo,
        past_player_club.apperances From past_player_club INNER JOIN Club on
        past_player_club.club_id = Club.club_id INNER JOIN Player ON
        past_player_club.player_id = Player.player_id ORDER BY Club.club ASC;
        """))


@app.route('/internationalawards')
def internationalawards():
    seen = ['test']
    return render_template(
        "internationalaward.html", seen=seen, results=sqlsetup(
            """SELECT Award.award, Award.award_photo, International.country,
            International_Award.count FROM International_Award INNER JOIN
            Award on International_Award.award_id = Award.award_id INNER JOIN
            International ON International_Award.international_id =
            International.International_id ORDER BY
            International_award.award_id ASC, International_Award.count DESC;
            """))


@app.route('/internationalapperances')
def internationalapperances():
    seen = ['test']
    return render_template(
        "internationalapperances.html", seen=seen, results=sqlsetup("""
        SELECT International.country, International.flag, Player.player,
        Player.photo, International_apperances.apperances FROM
        International_apperances INNER JOIN Player on
        International_apperances.player_id = Player.player_id INNER JOIN
        International ON International_apperances.international_id =
        International.International_id ORDER BY International.country ASC,
        International_apperances.apperances DESC;"""))


if __name__ == "__main__":
    app.run(debug=True)
