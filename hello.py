from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/name', methods=['POST'])
def hello_world():
    name = request.form.get('name')
    return render_template('hello.html',name=name)

@app.route('/name', methods = ['GET'])
def render_html():
    return render_template('form.html')