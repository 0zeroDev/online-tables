from models import Cell
from flask import Flask
from flask import render_template
from flask import request
from db_methods import Database
from sqlalchemy import inspect

app = Flask(
    __name__,
    template_folder='../frontend/',
    static_folder='../frontend',
    static_url_path=''
)

db = Database(engine='sqlite:///online-calc.db')
db_status = inspect(db.engine)
table_exists: bool = db_status.dialect.has_table(db.engine.connect(), "cells")
if not table_exists:
    print("table not exists! creating...")
    db.fill_table(db.create_empty_table(10, 10))


@app.route('/')
def index():
    return render_template(
        'table.html',
        title='Online Tables',
        cells=db.parse_cells()
    )


@app.route('/update_cell', methods=['POST'])
def update_cell():
    db.update_cell(x := int(request.form['cell_x']),
                   y := int(request.form['cell_y']),
                   content := request.form['cell_content'])

    # TODO(1): add Cell(x, y, content) to cells table and commit session

    return f'to_write: x={x}, y={y}, cell_content={content}'


if __name__ == "__main__":
    app.run(debug=True)
