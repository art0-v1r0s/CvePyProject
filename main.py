import os
from bottle import route, run, template, static_file, error, get, post, request
import mysql.connector
from sendMail import sendMailV2

error404Html = '''<!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="utf-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

                    <title>404 HTML Template by Colorlib</title>

                    <!-- Google font -->
                    <!--<link href="https://fonts.googleapis.com/css?family=Montserrat:700,900" rel="stylesheet"> -->


                    <link type="text/css" rel="stylesheet" href="css/style.css" />
                    <style>
                        * {
                  -webkit-box-sizing: border-box;
                          box-sizing: border-box;
                }

                body {
                  padding: 0;
                  margin: 0;
                }

                #notfound {
                  position: relative;
                  height: 100vh;
                  background: #030005;
                }

                #notfound .notfound {
                  position: absolute;
                  left: 50%;
                  top: 50%;
                  -webkit-transform: translate(-50%, -50%);
                      -ms-transform: translate(-50%, -50%);
                          transform: translate(-50%, -50%);
                }

                .notfound {
                  max-width: 767px;
                  width: 100%;
                  line-height: 1.4;
                  text-align: center;
                }

                .notfound .notfound-404 {
                  position: relative;
                  height: 180px;
                  margin-bottom: 20px;
                  z-index: -1;
                }

                .notfound .notfound-404 h1 {
                  font-family: 'Montserrat', sans-serif;
                  position: absolute;
                  left: 50%;
                  top: 50%;
                  -webkit-transform: translate(-50% , -50%);
                      -ms-transform: translate(-50% , -50%);
                          transform: translate(-50% , -50%);
                  font-size: 224px;
                  font-weight: 900;
                  margin-top: 0px;
                  margin-bottom: 0px;
                  margin-left: -12px;
                  color: #030005;
                  text-transform: uppercase;
                  text-shadow: -1px -1px 0px #8400ff, 1px 1px 0px #ff005a;
                  letter-spacing: -20px;
                }


                .notfound .notfound-404 h2 {
                  font-family: 'Montserrat', sans-serif;
                  position: absolute;
                  left: 0;
                  right: 0;
                  top: 110px;
                  font-size: 42px;
                  font-weight: 700;
                  color: #fff;
                  text-transform: uppercase;
                  text-shadow: 0px 2px 0px #8400ff;
                  letter-spacing: 13px;
                  margin: 0;
                }

                .notfound a {
                  font-family: 'Montserrat', sans-serif;
                  display: inline-block;
                  text-transform: uppercase;
                  color: #ff005a;
                  text-decoration: none;
                  border: 2px solid;
                  background: transparent;
                  padding: 10px 40px;
                  font-size: 14px;
                  font-weight: 700;
                  -webkit-transition: 0.2s all;
                  transition: 0.2s all;
                }

                .notfound a:hover {
                  color: #8400ff;
                }

                @media only screen and (max-width: 767px) {
                    .notfound .notfound-404 h2 {
                        font-size: 24px;
                    }
                }

                @media only screen and (max-width: 480px) {
                  .notfound .notfound-404 h1 {
                      font-size: 182px;
                  }
                }

                    </style>


                </head>

                <body>

                    <div id="notfound">
                        <div class="notfound">
                            <div class="notfound-404">
                                <h1>404</h1>
                                <h2>Page not found</h2>
                    </div>

                </body><!-- This templates was made by Colorlib (https://colorlib.com) -->

                </html>'''


# @route('/')
# def index():
#     return template(index_html, author='Real Python')

@error(404)
def error404(error):
    return template(error404Html)


@route('/show/user')
def show():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="rss"
    )
    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM user ')

    row = mycursor.fetchall()

    if row:
        return template('hello {{user}}', user=row)
    return HTTPError(404, "Page not found")


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='')


@route('/')
def homepage():
    return template('index.html')

@route('/csv')
def rss():
    return template('rss.html')


@route('/mail')
def addMail():
    return template('mail.html')


@post('/mailValidation')
def mailValidation():
    mail = request.forms.get('mail')
    sendMailV2(mail)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="rss"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO user(mail) VALUE('%s')"

    try:
        mycursor.execute(sql % (mail))
        mydb.commit()
    except:
        mydb.rollback()

    return template('mailValid', user=mail)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='localhost', port=port, debug=True)
