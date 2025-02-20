import os
import pyodbc
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Fetch connection string from Azure environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to Azure SQL Database
conn = pyodbc.connect(DATABASE_URL)

@app.route('/')
def index():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
