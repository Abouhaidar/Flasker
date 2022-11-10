# pip install flask
from flask import Flask

app=Flask(__name__)

##return HTML Tag with some styling
@app.route('/')
def firstpage():
    return '<h1 style={}>{}</h1>'.format("color:green;text-align:center;",'Hallo World!!!')

if __name__=='__main__':
    app.run(debug=True)