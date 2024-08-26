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


# updata data in the database given the databse item updated.
# table = the databse table in sql
# coullum = the coullum that is going to have a data changed
# item = the exact item in that coullum that will have a data update
# referance = a referance coullum in the database used for the where statement
# that will actual update
def update_data(table, coullum1, coullum2, item1, item2, referance):
    print(f"{table}\n{coullum1}\n{coullum2}\n{item1}\n{item2}\n{referance}")
    # find the original value for what we are going to increase by 1
    increase_sql = f"SELECT {referance} FROM {table} WHERE {coullum1} = ? and {coullum2} = ?;"
    # gain orginal number
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(increase_sql, (item1, item2))
    increase = cursor.fetchall()[0]
    addtion = int(increase[0]) + 1
    add = str(addtion)
    print(add)
    # sql query to update the value
    sql = f"UPDATE {table} SET {referance} = {add} WHERE {coullum1} = {item1} and {coullum2} = {item2};"
    print(sql)
    # complete the update
    # connect to the databse
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()


# add a new entry into the databse
# (the a winner of a trophy for the first time)
# table = the databse table in sql
# coullum 1,2,3 = each coullum in the complex many to many table
# item 1,2 = the other two values in the complex many to many
# eg. club id and award id
def add_data(table, coullum1, coullum2, coullum3, item1, item2):
    print(f"{table}\n{coullum1}\n{coullum2}\n{coullum3}\n{item1}\n{item2}")
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    # sql query to insert the new data into the databse
    sql = f"INSERT INTO {table} ({coullum1}, {coullum2}, {coullum3}) VALUES (?, ?, ?);"
    print(sql)
    cursor.execute(sql, (item1, item2, 1))
    db.commit()
    db.close()


# check and see if there is already a result in the database
# to see if add_data or update_data is needed
# table = the database table that is going to be updated
# coullum = a referances to check and see if the item we are looking for
# item = the exact team we are looking to find to confirm
# if update or add is needed
def check_data(table, coullum1, coullum2, item1, item2):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = f"SELECT * FROM {table} WHERE {coullum1} = ? and {coullum2} = ?;"
    print(sql)
    cursor.execute(sql, (item1, item2))
    results = cursor.fetchall()
    print(results)
    return results


# uppdate apperances needs one less data entry then update data
# so a new function is needed
def update_apperances(table, coullum1, coullum2, referance, item1):
    print(f"{table}\n{coullum1}\n{coullum2}\n{item1}\n{referance}")
    # find the original value for what we are going to increase by 1
    increase_sql = f"SELECT {coullum2}, {referance} FROM {table} WHERE {coullum1} = ?;"
    # gain orginal number
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(increase_sql, (item1,))
    increase = cursor.fetchall()
    checksql = "SELECT club_id FROM Player WHERE player_id = ?;"
    for item in increase:
        addtion = int(item[1]) + 1
        add = str(addtion)
        # sql query to update the value
        sql = f"UPDATE {table} SET {referance} = {add} WHERE {coullum2} = {item[0]} and {coullum1} = {item1};"
        # check and see if that player still plays for the clubthat just won
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute(checksql, (item[0],))
        check = cursor.fetchone()
        # if thnat club id in the player table = the club id in apperances
        # then it will increase the total apperances
        if check[0] == int(item1):
            # complete the update
            db = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            db.close()
            print("/// updated apperance ///")
        else:
            pass


# this will remove the first digit from an interger
def remover(removing):
    return removing[1:]


# this piece of code will update the total apperances number for players
# basied on the data inputed into the database,
# which means when a game gets added the toal apperance number will increase
# for all the players that played in that match
def update_total_apperances(table, coullum1, referance):
    find_total_app = "SELECT total_apperances FROM player"
    increase_sql = f"SELECT {referance} FROM {table} WHERE {coullum1} = ?;"
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    for i in range(1, len(sqlsetup(find_total_app)) + 1):
        count = 0
        cursor.execute(increase_sql, (i,))
        increase = cursor.fetchall()
        print(increase)
        for item in increase:
            for next in range(0, len(item)):
                count += item[next]
                print(count)
        interapp = f"SELECT {referance}s FROM international_apperances WHERE {coullum1} = ?;"
        cursor.execute(interapp, (i,))
        intapp = cursor.fetchone()
        print(intapp)
        if intapp is None:
            pass
        else:
            totalapp = count + intapp[0]
        print(totalapp)
        # final update
        sql = f"UPDATE Player SET total_apperances = {totalapp} WHERE {coullum1} = {i};"
        cursor.execute(sql)
        db.commit()


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
        # checks if a response is actual given to the form and
        # if it is blank, the full list will be displayed instead of nothing
        if splitplayer == ['']:
            return render_template("player.html", results=sqlsetup(order), fulllist=sqlsetup(order))
        else:
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
        # checks if a response is actual given to the form and
        # if it is blank, the full list will be displayed instead of nothing
        if splitclub == ['']:
            return render_template("club.html", results=sqlsetup(order), fulllist=sqlsetup(order))
        else:
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
        if splitinternational == ['']:
            return render_template("international.html", results=sqlsetup(order), fulllist=sqlsetup(order))
        else:
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
        # checks if a response is actual given to the form and
        # if it is blank, the full list will be displayed instead of nothing
        if splittrophy == ['']:
            return render_template("award.html", results=sqlsetup(query), fulllist=sqlsetup(query))
        else:
            for i in range(0, len(splittrophy)):
                cursor.execute(where, (splittrophy[i],))
                add = cursor.fetchall()
                results.extend(add)
            return render_template("award.html", results=results, fulllist=data, size=len(results))
    else:
        return render_template("award.html", results=data, fulllist=data)


# listing out all the players who a have played for a club and how,
# many apperances they have for that club
@app.route('/playerclubs')
def playerclubs():
    seen = ['test']
    return render_template("playerclubs.html", seen=seen, results=sqlsetup(
        """SELECT Club.club, Club.emblem, Player.player, Player.photo, club_apperances.apperance From club_apperances INNER JOIN Club on club_apperances.club_id = Club.club_id INNER JOIN Player ON club_apperances.player_id = Player.player_id ORDER BY Club.club ASC;
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


@app.route('/addnewgame', methods=['GET', 'POST'])
def addnewgame():
    award = str(request.get_data('trophies'))
    awardquery = "SELECT * FROM Award"
    awardwhere = awardquery
    awardwhere += " WHERE award_id =?"
    club1 = str(request.get_data('club1'))
    club2 = str(request.get_data('club2'))
    clubquery = 'SELECT Club.club_id, Club.club, Club.description, League.league, Club.emblem FROM Club INNER JOIN League ON Club.league_id = League.League_id'
    clubwhere = clubquery
    clubwhere += ' WHERE Club.club_id =?'
    cluborder = clubquery
    cluborder += ' ORDER BY Club.club ASC'
    if request.method == "POST":
        print(award + "\n" + club1 + "\n" + club2)
        print(type(award))
        checking = award.split("&")
        print(checking)
        # check and see if the game is being played for an award
        if len(checking) == 2:
            # split the data into the individual values
            splitclub1 = spliter(club1)
            splitclub2 = spliter(club2)
            # remove the extra digit added
            clubone = remover(splitclub1[0])
            clubtwo = remover(splitclub2[1])
        else:
            # split our responses to pure number values to be used to update
            # all the data needed
            splitaward = spliter(award)
            splitclub1 = spliter(club1)
            splitclub2 = spliter(club2)
            print(splitaward, "\n", splitclub1, "\n", splitclub2)
            # remove the extra digit added from form
            clubone = remover(splitclub1[1])
            clubtwo = remover(splitclub2[2])
            # check to see if the winer club has already one that thropy before
            if len(check_data("Club_Award", "club_id", "award_id", clubone, splitaward[0])) == 0:
                # adds a new data entry with the count of 1 to the Club_Award
                add_data("Club_Award", "club_id", "award_id", "count", clubone, splitaward[0])
            else:
                # increases the count number by one for that club winning
                # that award
                update_data("Club_Award", "club_id", "award_id", clubone, splitaward[0], "count")
        update_apperances("club_apperances", "club_id", "player_id", "apperance", clubone)
        update_apperances("club_apperances", "club_id", "player_id", "apperance", clubtwo)
        update_total_apperances("club_apperances", "player_id", "apperance")
        return render_template('addnewgame.html', sumbit='yes', testing='yes', awardlist=sqlsetup(awardquery), clublist=sqlsetup(cluborder))
    else:
        update_total_apperances("club_apperances", "player_id", "apperance")
        return render_template('addnewgame.html', submit='no', testing='yes', awardlist=sqlsetup(awardquery), clublist=sqlsetup(cluborder))


if __name__ == "__main__":
    app.run(debug=True)
