from datax_website import app
from flask import render_template, url_for, request, redirect


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/query_wait_time", methods=['POST'])
def query_wait_time():
    print(request.method)
    print("datetime: " + request.form.get('datetime') + " type: " + str(type(request.form.get('datetime'))))
    print("ride: " + request.form.get('ride') + " type: " + str(type(request.form.get('ride'))))
    return redirect(url_for('home'))