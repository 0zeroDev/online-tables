from models import Cell
from flask import Flask
from flask import render_template

from db_methods import Database

app = Flask(__name__, template_folder="../frontend/")

db = Database(engine='sqlite:///online-calc.db')

table = db.create_empty_table(2, 2)
for raw in table:
    db.fill_table(raw)

@app.route('/')
def index():
    html = render_template(
        'base.html',
        title='Online Tables',
        cells=[["1","1"], ["srtg", "ddes"]],
    )
    return html



# if __name__ == "__main__":
#     db = Database(engine='sqlite:///online-calc.db')
#     table = db.create_empty_table(2, 2)
#     for raw in table:
#         db.fill_table(raw)
#     db.parse_cells()