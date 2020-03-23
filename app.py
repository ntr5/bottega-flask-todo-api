from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os


app = Flask(__name__)
heroku = Heroku(app)
CORS(app)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://wuuvzyqrlyfjrq:0c95e309b21ce1b8bd3551c96154ac2789da4882b04a0242299a9ee13e923440@ec2-34-200-101-236.compute-1.amazonaws.com:5432/dc13k35695hikd"

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
        self.title = title
        self.done = done


class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "done")

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

# Post a todo
@app.route("/todo", methods=["POST"])
def add_todo():
    title = request.json["title"]
    done = request.json["done"]

    new_todo = Todo(title, done)

    db.session.add(new_todo)
    db.session.commit()

    todo = Todo.query.get(new_todo.id)
    return todo_schema.jsonify(todo)


@app.route("/todos", methods=["GET"])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)

    return jsonify(result)


# @app.route("/todo/<id>", methods=["GET"])
# def get_todo(id):
#     todo = Todo.query.get(id)
    
#     return todo_schema.jsonify(todo)


@app.route("/todo/<id>", methods=["PATCH"])
def update_todo(id):
    todo = Todo.query.get(id)

    new_done = request.json["done"]
    todo.done = new_done
    
    db.session.commit()
    return todo_schema.jsonify(todo)


@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()

    return jsonify("Todo Deleted")


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.debug = True
    app.run()