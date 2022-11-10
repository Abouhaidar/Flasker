from flask import Flask, request,render_template

app=Flask(__name__)

## saving Data in local file and return  saved  Data in Homepage
## creating text file not form app, else you delete all data inside it,
## after each new run u  create new file and replace old one

## return Template wiith input data, and return some logic text
@app.route('/',methods=['POST','GET'])
def app6home():
    with open('data/users.txt', 'r') as f:
        users = f.readlines()
        users=[name.strip().lower() for name in users]
    if request.method=='POST':
        name=request.form.get('username').strip().lower()
        if name and name!='':
            if name not in users:
                with open('data/users.txt','a') as f:
                    f.write(f"{name}\n")
                users.append(name)
    return render_template('app6_home.html',users=users)

if __name__=='__main__':
    app.run(debug=True)