from flask import Flask, request,render_template, flash
import pandas as pd
app=Flask(__name__)
app.secret_key='bm'
## to get flashed messages in HTMl you need secret_key
## return Template wiith input data, and return some logic text
@app.route('/',methods=['POST','GET'])
def home():
    ###use can use open(file.csv) in read modus and redlines users output=  list in list
    ### add user list append new list and to save data openfile then writeline --> save csv file
    users=pd.read_csv('data/users.csv')
    if request.method=='POST':
        name=request.form.get('name').strip().lower()
        age=request.form.get('age')
        location=request.form.get('location').strip().lower()
        if name and name!='':
            if name not in users.name.tolist():
                users=users.append(dict(name=name,age=age,location=location), ignore_index=True)
                users.to_csv('data/users.csv',index=False)
                flash('User Added!','green')
            else:
                flash('USer allready Exist','red')
    return render_template('home.html',users=users)
if __name__=='__main__':
    app.run(debug=True, port=5050)