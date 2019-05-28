import requests, json, pyodbc, matplotlib.pyplot as plt
from datetime import date, timedelta

def writeToJSONFile(path, data):
    with open(path, 'w', encoding="utf-8") as outfile:  
        json.dump(data, outfile, ensure_ascii=False)

def insertIntoDB(CURSOR, price, title, text, totalArea, kitchenArea, livingArea, location, rooms, addedOn):
    print("Price - ", price)
    print("Title - ", title)
    print("Text - ", text)
    print("Total Area - ", totalArea)
    print("Kitchen Area - ", kitchenArea)
    print("Living Area - ", livingArea)
    print("Location - ", location)
    print("Rooms - ", rooms)
    print("AddedOn - ", addedOn)
    
    CURSOR.execute("INSERT INTO postings (price_usd, title, text, total_area, kitchen_area, living_area, location, number_of_rooms, added_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", price, title, text, totalArea, kitchenArea, livingArea, location, rooms, addedOn)
    
    print("--------------------------------")

def getPesponses():
    d1 = date(2017, 1, 1)  # start date
    d2 = date(2017, 12, 31)  # end date

    delta = d2 - d1 

    responses = []

    for i in range(delta.days + 1):
        # print(d1 + timedelta(days=i))
        url = "https://35.204.204.210/" + str(d1 + timedelta(days=i)) + "/"
        print(url, end="\n\n")
        response = json.loads(requests.get(url, verify=False).text)
        responses.append(response)
    
    return responses

def drawPie(cursor):
    cursor.execute("SELECT DISTINCT [location] FROM postings")
    
    locations = []

    for row in cursor.fetchall():
        locations.append(row[0])
    print(locations)    

    posts_count = []

    for i in range(len(locations)):
        cursor.execute("SELECT price_usd FROM postings WHERE location=?", locations[i])
        posts = 0
        for row in cursor.fetchall():
            posts += 1

        posts_count.append(posts)

    plt.pie(posts_count, labels=locations, startangle=90, autopct='%.1f%%')
    plt.show()


def main():
    responses = getPesponses()
    # print(responses)

    conn = pyodbc.connect(driver='{SQL Server}', server='DESKTOP-90M435L', database='OLX', trusted_connection='yes')
    cursor = conn.cursor()

    for i in range(len(responses)):
        print("responses[{}]".format(i))
        response = responses[i]
        print("len response = {}".format(len(response["postings"])))
        if(len(response["postings"]) != 0):
            for j in range(len(response["postings"])):

                print("response[{}]".format(j))
                postings = response["postings"]
                insertIntoDB(cursor,
                        postings[j]["price_usd"],
                        postings[j]["title"],
                        postings[j]["text"],
                        postings[j]["total_area"],
                        postings[j]["kitchen_area"],
                        postings[j]["living_area"],
                        postings[j]["location"],
                        postings[j]["number_of_rooms"],
                        postings[j]["added_on"])
                conn.commit()
    
    drawPie(cursor)
    
#Start point
main()
