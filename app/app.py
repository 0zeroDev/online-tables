from models import Cell
from flask import Flask
from flask import render_template

from db_methods import Database

app = Flask(__name__, template_folder='../frontend/')


db = Database(engine='sqlite:///online-calc.db')

table = db.create_empty_table(2, 2)
for raw in table:
    db.fill_table(raw)

@app.route('/')
def index():
    return render_template(
        'table.html',
        title='Online Tables',
        cells=table
    )



if __name__ == "__main__":
    app.run(debug=True)