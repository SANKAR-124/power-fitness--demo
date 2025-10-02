from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import random


app=Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1246@localhost/pf_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__='contacts'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False)
    phone=db.Column(db.String(20), nullable=True)
    message=db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

class Quote(db.Model):
    __tablename__='qoutes'
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text, nullable=False)
    author=db.Column(db.String(200))


# --- Mail Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sankarkrishnap124@gmail.com'
app.config['MAIL_PASSWORD'] = 'cruw fpos elzs wuxm'
mail=Mail(app)

# Add this line for session security
app.config['SECRET_KEY'] = 'i_am studying_in_ahalia_school_of_engineering_and_technology'

@app.route('/')

def home():
    return render_template("index.html")

@app.route('/about')

def about():
    return render_template("about.html")

@app.route('/services')

def service():
    return render_template("service.html")

@app.route('/contact',methods=['GET','POST'])

def contact():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        new_submission=Contact(name=name,email=email,phone=phone,message=message)
        db.session.add(new_submission)
        db.session.commit()

        msg=Message(
            subject=f"New Contact from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
        )
        msg.body=f"FROM: {name} <{email}>\nphone: {phone}\n\n{message}"
        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template("contact.html")

# API route to get a random quote
@app.route('/api/random-quote')
def random_quote():
    # Get all qoutes from the database
    all_quotes = Quote.query.all()
    # Pick one at random from the list
    random_quote = random.choice(all_quotes)
    # Return the data in JSON format
    return jsonify({
        'text': random_quote.text,
        'author': random_quote.author
    })
# Add this new route for our success page
# @app.route('/thank-you')
# def thank_you():
#     return '<h1>Thank You!</h1><p>Your message has been received successfully.</p>'

if __name__=="__main__":
    app.run(debug=True)