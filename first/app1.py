# pip install flask
from flask import Flask

app=Flask(__name__)

##return HTML Tag
@app.route('/')
def firstpage():
    return '<h1>{}</h1>'.format('Hallo World!!!')

if __name__=='__main__':
    app.run(debug=True)