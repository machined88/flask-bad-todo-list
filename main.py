from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class toDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def main():
    todo_list = toDo.query.all()
    print(todo_list)
    return render_template("main.html", todo_list=todo_list)


@app.route("/add", methods=['POST'])
def add_item():
    title = request.form.get('title')
    new_todo = toDo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("main"))


@app.route("/delete/<int:todo_id>")
def delete_items(todo_id):
    todo = toDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main'))


@app.route("/update/<int:todo_id>")
def modify_items(todo_id):
    todo = toDo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("main"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
