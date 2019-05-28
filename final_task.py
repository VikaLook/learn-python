import requests, json, pyodbc

def writeToJSONFile(path, data):
    with open(path, 'w', encoding="utf-8") as outfile:  
        json.dump(data, outfile, ensure_ascii=False)

def insertIntoDB(CURSOR, price, title, text, totalArea, kitchenArea, livingArea, location, rooms, addedOn):
    if (title == ""):
        title="NO TITLE"
    
    print("Price - ", price)
    print("Title - ", title)
    print("Text - ", text)
    print("Total Area - ", totalArea)
    print("Kitchen Area - ", kitchenArea)
    print("Living Area - ", livingArea)
    print("Location - ", location)
    print("Rooms - ", rooms)
    print("AddedOn - ", addedOn)
    print("--------------------------------")

     

    CURSOR.execute("INSERT INTO postings VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(price, title, text, totalArea, kitchenArea, livingArea, location, rooms, addedOn))


response = json.loads(requests.get("https://35.204.204.210/2017-03-19/", verify=False).text)

print(len(response["postings"]))
print(response["postings"][0]["price_usd"])

# writeToJSONFile("data.json", response)

conn = pyodbc.connect(driver='{SQL Server}', server='DESKTOP-90M435L', database='OLX', trusted_connection='yes')

cursor = conn.cursor()
# cursor.execute('SELECT * FROM postings')

for i in range(len(response["postings"]) - 1):
    print(i)
    insertIntoDB(cursor,
                 response["postings"][i]["price_usd"],
                 response["postings"][i]["title"],
                 response["postings"][i]["text"],
                 response["postings"][i]["total_area"],
                 response["postings"][i]["kitchen_area"],
                 response["postings"][i]["living_area"],
                 response["postings"][i]["location"],
                 response["postings"][i]["number_of_rooms"],
                 response["postings"][i]["added_on"])
    
    conn.commit()

# cursor.execute('SELECT * FROM postings WHERE price_usd=1')
# # conn.commit()
# for row in cursor.fetchall():
#     print('row = %r' % (row,))
