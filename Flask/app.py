from flask import Flask, render_template, request, redirect
import smtplib
import ssl
import pymysql
from email.message import EmailMessage
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
userpass = 'mysql+pymysql://root:@'
basedir  = '127.0.0.1'
dbname   = '/NewDB'
socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
dbname   = dbname + socket
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#initialise db
db = SQLAlchemy(app)

#create db Model
class Friends(db.Model):      #To make the database run " flask shell " then " db.create_all() "
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    date_of_creation = db.Column(db.DateTime, default = datetime.utcnow)
    #create a function that returns a string when data is added into the database
    def __repr__(self):
        return '<Name %r>' % self.id

subscribers = []
 
@app.route('/')
def index():
    return render_template("index.html") 
@app.route('/friends', methods=['POST','GET'])
def friends():
    title = "My Friend's list"
    if request.method == "POST":
        fName = request.form.get("name")
        nFriend = Friends(name=fName)
        #push to database
        try:
            db.session.add(nFriend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding your friend" 
    else:
        Dost = Friends.query.order_by(Friends.date_of_creation)
        print(Dost)
        return render_template("friends.html",title=title, dost=Dost) 
    

@app.route('/about')
def about():
    title = "About Me"
    names = ["Aman", "Abhinesh", "Piyush"]
    return render_template("about.html",names=names, title=title)

@app.route('/subscribe')
def subscribe():
    title = "Subscribe"
    return render_template("subscribe.html", title = title)

@app.route('/form', methods = ["POST"])
def form():
    first= request.form.get("First Name")
    second= request.form.get("Second Name")
    email= request.form.get("Email")
    title = "Thank You"
    if not first or not second or not email:
        errorStatement = " All fields are compulsory to fill "
        return render_template( "subscribe.html", error=errorStatement, first =first, second = second, email=email)
    subscribers.append(f"{first} {second} || {email}")
    
    senderEmail = "piyush.uprety@gmail.com"
    appPassword = "auiltohajxxfcqzk"
    subject = "Conformation Mail"
    body = "You have subscribed to our newsletter"
    
    em = EmailMessage()
    em['From'] = senderEmail
    em['To'] = email
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(senderEmail, appPassword)
        smtp.sendmail(senderEmail, email, em.as_string())

    return render_template("form.html", title=title, firstName = first, secondName = second, email= email)

@app.route('/ourSubcribers')
def showSubs():
    count = len(subscribers)
    title= "Our Subcribers"
    return render_template("ourSubs.html", subs = subscribers, count= count, title=title)