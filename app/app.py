from models import Cell
from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder="../frontend/")


@app.route('/')
def index():
    html = render_template(
        'base.html',
        title='Online Tables',
        cells=[0, 0],
    )
    return html
