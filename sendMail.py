import smtplib

def sendMail(mail): ##function a envoyer mail

    serveur = smtplib.SMTP('smtp.gmail.com', 587)    ## Connexion au serveur sortant (en précisant son nom et son port)
    serveur.starttls()    ## Spécification de la sécurisation
    fromadd = 'arthurjunior20202@gmail.com'
    password = 'hunterXhunter20'
    toadd = mail
    message = 'Bonjour \nMerci de vous avoir abonnes a notre newsletter'
    serveur.login(fromadd,password)    ## Authentification

    serveur.sendmail(fromadd , toadd , message)    ## Envoie du message

    serveur.quit()    ## Déconnexion du serveur

    return "EXIT_SUCCESS"