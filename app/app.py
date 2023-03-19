from models import Cell
from flask import Flask
from flask import render_template
from flask import request
from db_methods import Database
from sqlalchemy import inspect
from arifmetics import calculate_expression

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
def index():
    cells_matrix: list[list[Cell]] = db.parse_cells()

# TODO:
#    Первый вариант - посылать y в формате текста
#    Второй вариант - конвертировать y в текст на стороне клиента (возможно так будет легче)
#    x = [[cell.x for cell in row] for row in table],
#    y = [[chr(cell.y + 64) for cell in row] for row in table],
#    content = [[cell.content for cell in row] for row in table]

    return render_template(
        'table.html',
        title='Online Tables',
        cells=cells_matrix,
    )


@app.route('/update_cell', methods=['POST'])
def update_cell():
    db.update_cell(
        x := int(request.form['cell_x']),
        y := int(request.form['cell_y']),
        content := request.form['cell_content']
    )

    calculated_content: str = calculate_expression(content)
    db.update_cell(x, y, calculated_content)
    return calculated_content


if __name__ == "__main__":
    app.run(debug=True)
