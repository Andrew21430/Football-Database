import sqlite3

trophy = "?tropies=6&tropies=7&tropies=8"
splittrophy = trophy.split("&")
for i in range(0, len(splittrophy)):
    splittrophy[i] = filter(str.isdecimal, str(splittrophy[i]))
    splittrophy[i] = "".join(splittrophy[i])
print(splittrophy)


DATABASE = "Database.db"
db = sqlite3.connect(DATABASE)
cursor = db.cursor()
results = []
for i in range(0, len(splittrophy)):
    cursor.execute("SELECT * FROM Award WHERE award_id =?", (splittrophy[i],))
    results.extend(cursor.fetchall())

print(results)
for test in results:
    print(test[0], test[1], test[2], test[3])
