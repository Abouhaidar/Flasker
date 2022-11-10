# pip install flask
from flask import Flask

app=Flask(__name__)

# return sample text
@app.route('/')
def firstpage():
    return 'Hallo world'

if __name__=='__main__':
    app.run(debug=True)