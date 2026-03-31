from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/submit-signin', methods=['POST'])
def index_formsubmitted():
    if request.method == 'POST':
        form_data = request.form
        print(f"Received data: {dict(form_data)}") # Log the data on the server
        return render_template('indexwsignin.html.jinja', username=form_data['username'])

if __name__ == '__main__':
    app.run(debug=True)