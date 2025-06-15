import csv
import sqlite3

# con = sqlite3.connect("jarvis.db")
# cursor = con.cursor()
with sqlite3.connect("jarvis.db") as con:
    cursor = con.cursor()
    # cursor.execute(...)
# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key , name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key , name VARCHAR(100),url path VARCHAR(1000))"
# cursor.execute(query)

# # #opening non-system apps
# query = "INSERT INTO sys_command VALUES (null, 'android studio', 'C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe')"
# cursor.execute(query)
# con.commit()
 
#downloads query must be deleted and wiki pedia query also

#Opening Web apps
# query = "INSERT INTO web_command VALUES (null, 'github', 'https://github.com/')"
# # cursor.execute(query)
# cursor.execute("DELETE FROM contacts WHERE id = 1")
# cursor.execute("DELETE FROM contacts WHERE id = 3")
# cursor.execute("DELETE FROM contacts WHERE id = 4")
# con.commit()


#### 1. Create contacts Table 
# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# 2. Import CSV file into database
# Specify the column indices you want  to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 20]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# #### 4. Insert Single contacts (Optional)
query = "INSERT INTO contacts VALUES (null,'Pareshu', '8380005811', 'null')"
cursor.execute(query)
# cursor.execute("DELETE FROM contacts WHERE id = 5")
# cursor.execute("DELETE FROM contacts WHERE id = 8")

# con.commit()

#### 5. Search Contacts from database
# query = 'sam'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])
