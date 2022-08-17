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
    conn.rollback()
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
                    return redirect (url_for("admin"))

    return render_template("index.html")


@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")


@app.route('/new_user', methods=["GET","POST"])
def new_user():

   if "user" in session:

    c.execute("""SELECT * FROM users""")
    users_select = c.fetchall()
    conn.commit()
    user_list = []
    for i in range(len(users_select)):
        each_user=[users_select[i][0],users_select[i][1],users_select[i][2]]
        user_list.append(each_user)


    if request.method=="POST":
        if request.form.get("delete")=="delete":
            username_to_delete=request.form.get("username_table")
            c.execute("""DELETE FROM users WHERE username='{value1}'""".format(value1=username_to_delete))
            conn.commit()
            return redirect(url_for("new_user", users=user_list, name=username_to_delete))

        if request.form.get("create")=="create":
            username = request.form.get("username")
            password = request.form.get("password")
            user_type = request.form.get("user_type")
            c.execute("""INSERT INTO users(username,password,user_type) VALUES('{value1}','{value2}','{value3}')""".format(value1=username,value2=password,value3=user_type))
            conn.commit()
        
        if request.form.get("edit")=="edit":
            session['username_to_edit'] = request.form.get("username_table")
            return redirect(url_for("user_edit"))


    return render_template("new_user.html", users=user_list)
   return render_template("index.html")
    
@app.route('/user_edit', methods=["GET","POST"])
def user_edit():
    
    username_to_edit=session['username_to_edit']

    c.execute("""SELECT * FROM users""")
    users_select = c.fetchall()
    conn.commit()
    user_list = []
    for i in range(len(users_select)):
        each_user=[users_select[i][0],users_select[i][1],users_select[i][2]]
        user_list.append(each_user)

    if request.method=="POST":
        username = request.form.get("username_edit")
        password = request.form.get("password_edit")
        user_type = request.form.get("user_type_edit")
        c.execute("""UPDATE users SET username='{value1}',password='{value2}',user_type='{value3}' WHERE username='{value4}'""".format(value1=username,value2=password,value3=user_type, value4=username_to_edit))
        conn.commit()
        session.pop('username_to_edit')

        return redirect(url_for("new_user", users=user_list))
    return render_template("user_edit.html")

    

if __name__ == '__main__':
    app.run(debug=True)