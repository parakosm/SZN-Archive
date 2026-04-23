from flask import Flask, render_template, request, make_response
import sqlite3

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
        database = sqlite3.connect("Database\database.db")
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
        database = sqlite3.connect("Database\database.db")
        cursor = database.cursor()
        dob = f"{form_data['dd']}-{form_data['mm']}-{form_data['yyyy']}"
        cursor.execute("INSERT INTO Users (username, email, password, DOB) VALUES (?, ?, ?, ?)", (form_data['username'], form_data['email'], form_data['password'], dob))
        database.commit()
        database.close()
        signup = make_response(render_template('indexwsignup.html.jinja', username=form_data['username']))
        signup.set_cookie("User", form_data['username'])
        return signup

if __name__ == '__main__':
    app.run(debug=True)
