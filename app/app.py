from models import Cell
from flask import Flask
from flask import render_template
from flask import request
from db_methods import Database

app = Flask(__name__, template_folder='../frontend/')
db = Database(engine='sqlite:///online-calc.db')
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
    x = request.form['cell_x']
    y = request.form['cell_y']
    content = request.form['cell_content']

    return f'to_write: x={x}, y={y}, cell_content={content}'


if __name__ == "__main__":
    app.run(debug=True)
