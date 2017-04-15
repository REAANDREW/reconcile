from flask import render_template
from skeleton_python_system import app


@app.route('/')
def index():
  return render_template('index.html', title='reconcile')
