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
def update_data(table, coullum1, coullum2, item1, item2, referance):
    print(f"{table}\n{coullum1}\n{coullum2}\n{item1}\n{item2}\n{referance}")
    # connect to the databse
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    # find the original value for what we are going to increase by 1
    increase_sql = f"SELECT {referance} FROM {table} WHERE {coullum1} = ? and {coullum2} = ?;"
    # gain orginal number
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(increase_sql, (item1, item2))
    increase = cursor.fetchall()[0]
    # sql query to update the value
    sql = f"UPDATE {table} SET {referance} = ? WHERE {coullum1} = ? and {coullum2} = ?;"
    print(sql)
    # complete the update
    addtion = int(increase[0]) + 1
    add = str(addtion)
    print(add)
    cursor.execute(sql, (add, item1, item2,))


# add a new entry into the databse
# (the a winner of a trophy for the first time)
# table = the databse table in sql
# coullum 1,2,3 = each coullum in the complex many to many table
# item 1,2 = the other two values in the complex many to many
# eg. club id and award id
def add_data(table, coullum1, coullum2, coullum3, item1, item2):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    # sql query to insert the new data into the databse
    sql = f"INSERT INTO {table} ({coullum1}, {coullum2}, {coullum3}) VALUES (?, ?, ?);"
    cursor.execute(sql, (item1, item2, 1))


# check and see if there is already a result in the database
# to see if add_data or update_data is needed
# table = the database table that is going to be updated
# coullum = a referances to check and see if the item we are looking for
# item = the exact team we are looking to find to confirm
# if update or add is needed
def check_data(table, coullum, item):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = f"SELECT * FROM {table} WHERE {coullum} = ?;"
    cursor.execute(sqlsetup(sql, (item,)))
    results = cursor.fetchall()
    if results is None:
        return (False)
    else:
        return (True)


update_data("Club_Award", "club_id", "award_id", 11, 1, "count")

add_data("Club_Award", "club_id", "award_id", "count", 69, 1)
