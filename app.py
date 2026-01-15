from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sn} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def show():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/edit/<int:sn>", methods=['GET', 'POST'])
def edit(sn):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sn=sn).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sn=sn).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sn>")
def delete(sn):
    todo = Todo.query.filter_by(sn=sn).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    # app.run(debug=True, port=8000) # port:optional, for other
    app.run(debug=False, use_reloader=False, port=8000)

@app.cli.command("create_db")
def create_db():
    db.create_all()
    print("Database created!")
