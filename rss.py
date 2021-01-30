import feedparser
from bs4 import BeautifulSoup
import requests
import mysql.connector

# import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="rss"
)

mycursor = mydb.cursor()


url = "https://www.cert.ssi.gouv.fr"
reponse = requests.get(url)
page = reponse.content
soup = BeautifulSoup(page)
linkRss = []
for linkFeeds in soup.find_all('a'):
    linkFeed = linkFeeds.get('href')
    if "/feed/" in linkFeed:
        linkRss.append(linkFeed)
        ##permet d'avoir dans une liste tous les liens feeds

linkRss.remove("/dur/feed/")  ##enleve de la liste le lien ou l'on na pas acces "forbidden not permitted"

linkDescriptionCve = []

for i in range(len(linkRss)):

    link = "https://www.cert.ssi.gouv.fr" + linkRss[i]
    rss = feedparser.parse(link)
    size = len(rss.entries)
    for i in range(size):

        linkCve = rss.entries[i].link
        #print(linkCve)
        reponse = requests.get(linkCve)
        page = reponse.content
        soup = BeautifulSoup(page)

        linkDescriptionCve.append(linkCve)
        count: int = 0

        for descript in soup.find_all('td'):
            #print(descript.string)

            linkDescriptionCve.append(descript.string)
            count = count + 1
            #print(count)
            if 12 == count:

                sql = "SELECT reference FROM cert Where reference = '%s'"

                mycursor.execute(sql % (linkDescriptionCve[2]))
                rows = mycursor.fetchall()
                results = len(rows)

                if results == 0:
                    sql = "INSERT INTO cert (link,reference,titre,premVers,dernVers) VALUES ('%s' ,'%s' ,'%s' ,'%s' ,'%s');"
                    mycursor.execute(sql % (
                    linkCve, linkDescriptionCve[2], linkDescriptionCve[4], linkDescriptionCve[6],
                    linkDescriptionCve[8]))
                    print(linkDescriptionCve)
                    # data = {
                    #
                    #     {
                    #         "id": "2702",
                    #         "link": "test1",
                    #         "reference": "test1",
                    #         "titre": "test1",
                    #         "premVers": "21 décembre 2000",
                    #         "dernVers": "21 décembre 2000"
                    #
                    #     },
                    #
                    # }
                    # with open('cert.json','w') as write_file:
                    #      json.dump(linkDescriptionCve, write_file)
                    try:
                        mycursor.execute(sql % (
                        linkCve, linkDescriptionCve[2], linkDescriptionCve[4], linkDescriptionCve[6],
                        linkDescriptionCve[8]))
                        mydb.commit()
                    except:
                        mydb.rollback()
                print("supression disct")
                del linkDescriptionCve[:]
