from flask import Flask, request,render_template
import pandas as pd
app=Flask(__name__)

## return Template wiith input data, and return some logic text
@app.route('/',methods=['POST','GET'])
def home():
    users=pd.read_csv('data/users.csv')
    msg=None
    if request.method=='POST':
        name=request.form.get('name').strip().lower()
        age=request.form.get('age')
        location=request.form.get('location').strip().lower()
        if name and name!='':
            if name not in users.name.tolist():
                users=users.append(dict(name=name,age=age,location=location), ignore_index=True)
                users.to_csv('data/users.csv',index=False)
                msg='User Added!'
            else:
                msg='USer allready Exist'
    return render_template('home.html',users=users,msg=msg)
if __name__=='__main__':
    app.run(debug=True)