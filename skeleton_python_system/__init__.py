from flask import Flask
app = Flask(__name__, static_url_path='/static')

import skeleton_python_system.views
