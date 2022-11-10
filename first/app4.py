from flask import Flask, request,render_template

app=Flask(__name__)

## return Template
## how it work: localhost/?name=Usernamme //Example: http://127.0.0.1:5000/?name=John%20Smith
@app.route('/')
def firstpage():
    name=request.args.get('name','John')
    return render_template('app4_home.html',name=name)


if __name__=='__main__':
    app.run(debug=True)