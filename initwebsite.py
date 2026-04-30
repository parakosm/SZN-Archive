from flask import Flask, render_template, request, make_response
import sqlite3
import os

basedir = os.path.dirname(os.path.abspath(__file__))
dbpath = os.path.join(basedir, "Database", "database.db")

app = Flask(__name__)

@app.route('/')
def index():
    user = request.cookies.get('User')
    if user is None:
        user = "None"
    return render_template('index.html.jinja', user=user)

@app.route('/submit-signin', methods=['POST'])
def index_signinsubmitted():
    if request.method == 'POST':
        form_data = request.form
        print(f"Sign in attempt: {dict(form_data)}") 
        database = sqlite3.connect(dbpath)
        cursor = database.cursor()
        cursor.execute(f"SELECT password FROM Users WHERE username = \'{form_data['username']}\'")
        user = cursor.fetchone()
        database.close()
        try:
            if user[0] == form_data['password']:
                signin = make_response(render_template('indexwsignin.html.jinja', username=form_data['username']))
                signin.set_cookie("User", form_data['username'])
                return signin
            else:
                return render_template('indexwsigninfail.html.jinja')
        except:
            return render_template('indexwsigninfail.html.jinja')

@app.route('/submit-signup', methods=['POST'])
def index_signupsubmitted():
    if request.method == 'POST':
        form_data = request.form
        print(f"Sign up attempt: {dict(form_data)}") 
        database = sqlite3.connect(dbpath)
        cursor = database.cursor()
        dob = f"{form_data['dd']}-{form_data['mm']}-{form_data['yyyy']}"
        cursor.execute("INSERT INTO Users (username, email, password, DOB) VALUES (?, ?, ?, ?)", (form_data['username'], form_data['email'], form_data['password'], dob))
        database.commit()
        database.close()
        signup = make_response(render_template('indexwsignup.html.jinja', username=form_data['username']))
        signup.set_cookie("User", form_data['username'])
        return signup
        
@app.route('/upload')
def upload():
    user = request.cookies.get('User')
    if user is None:
        user = "None"
    return render_template('upload.html.jinja', user=user)

@app.route('/submit-song', methods=['POST'])
def upload_songsubmitted():
    if request.method == 'POST':
        form_data = request.form
        print(f"Upload attempt: {dict(form_data)}")
        database = sqlite3.connect(dbpath)
        cursor = database.cursor()
        title = form_data['title']
        release = form_data['release']
        streaminglink = form_data['streaminglink']
        forfansof = form_data['FFO']
        user = request.cookies.get('User')
        cursor.execute("SELECT songid FROM Songs")
        ids_available = cursor.fetchall()
        ids_available = [row[0] for row in ids_available]
        newid = max(ids_available) + 1
        cursor.execute("INSERT INTO Songs (username, songid, streaminglink, title, release, FFO) VALUES (?, ?, ?, ?, ?, ?)", (user, newid, streaminglink, title, release, forfansof))
        database.commit()
        database.close()
        return render_template('uploadsuccess.html.jinja', user=user)
    
@app.route('/browse')
def browse():
    user = request.cookies.get('User')
    if user is None:
        user = "None"
    return render_template('browse.html.jinja', user=user)

@app.route('/browse-unrated')
def browseunrated():
    user = request.cookies.get('User')
    if user is None:
        user = "None"
    database = sqlite3.connect(dbpath)
    cursor = database.cursor()
    cursor.execute("SELECT songid FROM Songs")
    allsongids = cursor.fetchall()
    allsongids = [row[0] for row in allsongids]
    cursor.execute("SELECT songid FROM Ratnings")
    ratedsongids = cursor.fetchall()
    ratedsongids = [row[0] for row in ratedsongids]
    unratedsongids = list(set(allsongids) ^ set(ratedsongids))
    song = unratedsongids.choice()
    cursor.execute(f"SELECT title FROM Songs WHERE songid = \'{song}\'")
    title = cursor.fetchone()
    cursor.execute(f"SELECT release FROM Songs WHERE songid = \'{song}\'")
    release = cursor.fetchone()
    cursor.execute(f"SELECT streaminglink FROM Songs WHERE songid = \'{song}\'")
    streaminglink = cursor.fetchone()
    cursor.execute(f"SELECT FFO FROM Songs WHERE songid = \'{song}\'")
    forfansof = cursor.fetchone()
    database.close()
    return render_template('rate.html.jinja', user=user, title=title, release=release, streaminglink=streaminglink, forfansof=forfansof)

@app.route('/browse-rated')
def browserated():
    if request.method == 'POST':
        user = request.cookies.get('User')
        if user is None:
            user = "None"

        form_data = request.form
        database = sqlite3.connect(dbpath)
        cursor = database.cursor()
        cursor.execute("SELECT songid FROM Songs")
        allsongids = cursor.fetchall()
        allsongids = [row[0] for row in allsongids]
        songfound = False
        while songfound == False:
            song = allsongids.choice()
            cursor.execute(f"SELECT rating FROM Ratings WHERE songid = \'{song}\'")
            ratings = cursor.fetchall()
            ratings = [row[0] for row in ratings]
            rating = sum(rating) / len(rating)
            if rating >= form_data["minimum"] and rating <= form_data["maximum"]:
                songfound = True
        cursor.execute(f"SELECT title FROM Songs WHERE songid = \'{song}\'")
        title = cursor.fetchone()
        cursor.execute(f"SELECT release FROM Songs WHERE songid = \'{song}\'")
        release = cursor.fetchone()
        cursor.execute(f"SELECT streaminglink FROM Songs WHERE songid = \'{song}\'")
        streaminglink = cursor.fetchone()
        cursor.execute(f"SELECT FFO FROM Songs WHERE songid = \'{song}\'")
        forfansof = cursor.fetchone()
        database.close()
        return render_template('rate.html.jinja', user=user, title=title, release=release, streaminglink=streaminglink, forfansof=forfansof, rating=rating)

if __name__ == '__main__':
    app.run(debug=True)