import smtplib, ssl
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendMail(mail):  ##function a envoyer mail
    data = recupData()
    print(data)
    serveur = smtplib.SMTP('smtp.gmail.com', 587)  ## Connexion au serveur sortant (en précisant son nom et son port)
    serveur.starttls()  ## Spécification de la sécurisation
    fromadd = 'arthurjunior20202@gmail.com'
    password = 'hunterXhunter20'
    toadd = mail
    message = 'Bonjour \nMerci de vous avoir abonnes a notre newsletter\n voici le lien vers notre dernier donnee enregistrer : ' + \
              data[1]
    print(message)
    serveur.login(fromadd, password)  ## Authentification

    serveur.sendmail(fromadd, toadd, message)  ## Envoie du message

    serveur.quit()  ## Déconnexion du serveur

    return "EXIT_SUCCESS"


def sendMailV2(mail):
    data = recupData()
    sender_email = 'arthurjunior20202@gmail.com'
    receiver_email = mail
    password = 'hunterXhunter20'

    message = MIMEMultipart()
    message["Subject"] = "Newsletter Python CVE"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = "Bonjour,\n\nMerci de vous avoir abonnez a notre newsletter.\nCi dessous le site : http://localhost:8080\nVoici notre derniere donné entrée %s \nCordialement PyhonCVE" % (
    data[1])

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def recupData():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="rss"
    )

    mycursor = mydb.cursor()

    sql = "select * from cert where id >= all ( select id from cert order by id desc )"

    mycursor.execute(sql)

    return mycursor.fetchone()


sendMailV2('arthurd2000@gmail.com')
