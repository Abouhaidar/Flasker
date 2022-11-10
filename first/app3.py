# pip install flask
from flask import Flask, request

app=Flask(__name__)

## return Userinput if None return Hallo John
## how it work: localhost/?name=Usernamme
@app.route('/')
def firstpage():
    name=request.args.get('name','John')
    return '<h1 style={}>Hallo {}!!!</h1>'.format("color:green;text-align:center;",name)

## how it work: localhost/user/?name=Usernamme&age=43
@app.route('/user/')
def user():
    name=request.args.get('name','John')
    age=request.args.get('age',30)
    return '<h1 style={}>Hallo {} your are {} years old!!!</h1>'.format("color:green;text-align:center;",name,age)

if __name__=='__main__':
    app.run(debug=True)