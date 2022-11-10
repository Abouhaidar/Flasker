from flask import Flask, request,render_template

app=Flask(__name__)

## return Template wiith input data, and return some logic text
@app.route('/',methods=['POST','GET'])
def app5home():
    name=None
    if request.method=='POST':
        name=request.form.get('username')
    return render_template('app5_home.html',name=name)


if __name__=='__main__':
    app.run(debug=True)