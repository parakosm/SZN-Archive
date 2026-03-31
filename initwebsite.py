from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/submit-signin', methods=['POST'])
def index_signinsubmitted():
    if request.method == 'POST':
        form_data = request.form
        print(f"Sign up: {dict(form_data)}") 
        return render_template('indexwsignin.html.jinja', username=form_data['username'])
    
@app.route('/submit-signup', methods=['POST'])
def index_signupsubmitted():
    if request.method == 'POST':
        form_data = request.form
        print(f"Sign up: {dict(form_data)}") 
        return render_template('indexwsignup.html.jinja', username=form_data['username'])

if __name__ == '__main__':
    app.run(debug=True)