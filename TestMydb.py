import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="rss"
)

mycursor = mydb.cursor()

data = ['https://www.cert.ssi.gouv.fr/alerte/CERTFR-2020-ALE-003/', 'Référence','CERTFR-2020-ALE-003', 'Titre','Vulnérabilité dans les produits Mozilla', 'Date de la première version', '09 janvier 2020', 'Date de la dernière version','20 janvier 2020']


sql = "INSERT INTO cert (link,reference,titre,premVers,dernVers) VALUES ('%s' ,'%s' ,'%s' ,'%s' ,'%s');"

try:
    mycursor.execute(sql % (data[0], data[2], data[4], data[6], data[8]))
    mydb.commit()
except:
    mydb.rollback()
