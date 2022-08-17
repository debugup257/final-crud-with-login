from flask import Flask, render_template, render_template_string, request,redirect,url_for,session
import psycopg2
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key="hello"

conn = psycopg2.connect(
   database="d67fsm4svq5gp3", user='cthlqzrfduldux', password='284d42f2d7277cf2318c7053bb11f6665c3ba385f1abc9ca3668af049a5eb06e', host='ec2-44-195-100-240.compute-1.amazonaws.com', port= '5432'
)
c = conn.cursor()

@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        c.execute("SELECT username FROM users;")
        usernames = (c.fetchall())
        usernames_list=[]

        for i in usernames:
            usernames_list.append(i[0])
        conn.commit()
        
        c.execute("SELECT password FROM users;")
        passwords = (c.fetchall())
        passwords_list=[]

        for i in passwords:
            passwords_list.append(i[0])
        conn.commit()

        if username in usernames_list:
            if password in passwords_list:
                session.permanent=False
                session["user"]=username
                c.execute("""SELECT user_type FROM users WHERE username = %(value)s; """,{"value":username})
                user_type = (c.fetchall())
                if user_type[0][0]=="admin":
                    return "success"

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)