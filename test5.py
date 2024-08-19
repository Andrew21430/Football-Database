import sqlite3


DATABASE = "Database.db"


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
def update_data(table, coullum1, coullum2, referance, item1, item2):
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
        print(add)
        # sql query to update the value
        sql = f"UPDATE {table} SET {referance} = {add} WHERE {coullum2} = {item[0]} and {coullum1} = {item1};"
        print(sql)
        # check and see if that player still plays for the clubthat just won
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute(checksql, (item[0],))
        check = cursor.fetchone()
        # if thnat club id in the player table = the club id in apperances
        # then it will increase the total apperances
        if check[0] == item1:
            print("passed")
            # complete the update
            db = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            db.close()
        else:
            print('passed')


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
        count + int(cursor.execute(interapp, (i,)))
        print(count)
        # final update
        sql = f"UPDATE Player SET total_apperance = {count} WHERE {coullum1} = {i};"
        cursor.execute(sql)
        db.commit()


'''check_data("Club_Award", "club_id", "award_id", 118, 2)
if len(check_data("Club_Award", "club_id", "award_id", 118, 2)) == 0:
    print("add")
    add_data("Club_Award", "club_id", "award_id", "count", 118, 2)
else:
    print("update")
    update_data("Club_Award", "club_id", "award_id", "count", 118, 2)

update_apperances("club_apperances", "club_id", "player_id", "apperance", 118)'''

update_total_apperances("club_apperances", "player_id", "apperance")
