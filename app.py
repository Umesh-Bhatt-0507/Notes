from sqlalchemy import URL
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

url=URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="@1616856423Umesh",
    host="localhost",
    port=5433,
    database="Notes",
)

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="ashu"
db=SQLAlchemy(app)

class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    content=db.Column(db.Text)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

@app.route('/')
def home():
    notes=Note.query.all()
    return render_template("home.html",notes=notes)

@app.route('/add',methods=["GET","POST"])
def add():
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        note=Note(
            title=title,
            content=content,
        )
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_note.html")

@app.route('/delete/<int:id>')
def delete(id):
    note=Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("home"))






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)