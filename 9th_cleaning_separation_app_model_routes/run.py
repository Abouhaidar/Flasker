from flasker import app, db
from flasker.models import Users, Posts
with app.app_context():
    db.create_all()
if __name__=='__main__':
    app.run(debug=True, port=5200)

