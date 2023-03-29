from models import Cell
from flask import Flask
from flask import render_template
from flask import request
from db_methods import Database
from sqlalchemy import inspect
from arifmetics import calculate_expression, is_formula

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
    print("Table not exists! creating...")
    db.fill_table(db.create_empty_table(10, 10))


@app.route('/')
def index() -> str:
    cells_matrix: list[list[Cell]] = db.parse_cells()

    return render_template(
        'table.html',
        title='Online Tables',
        cells=cells_matrix,
    )


@app.route('/update_cell', methods=['POST'])
def update_cell() -> str:
    db.update_cell(
        x := int(request.form['cell_x']),
        y := int(request.form['cell_y']),
        updated_content := str(request.form['cell_content'])
    )

    if is_formula(updated_content):
        db.update_cell(x, y, updated_content)
        return calculate_expression(updated_content)

    return updated_content


if __name__ == "__main__":
    app.run(debug=True)
