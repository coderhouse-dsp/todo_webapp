from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import urllib

app = Flask(__name__)

# Azure SQL Database connection string
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:patelde-server.database.windows.net,1433;Database=todo_db;Uid=patelde-server-admin;Pwd=password;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
params = urllib.parse.quote_plus(connection_string)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form['task']
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'id': new_todo.id, 'task': new_todo.task})

if __name__ == '__main__':
    app.run(debug=True)