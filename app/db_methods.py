from models import Base, Cell
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, func
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, engine: str) -> None:
        self.engine = create_engine(engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        
    def fill_table(self, table: list[list[Cell]]) -> None:
        Base.metadata.create_all(self.engine)
 
        try:
            for row in table:
                self.session.add_all(row)
            self.session.commit()
        except IntegrityError as e:
            print("Objects alredy exists...", e)

    
    def parse_cells(self) -> list[list[Cell]]:
        """
        Returns matrix of cells parsed from cells table.
        """
        cells: list[Cell] = self.session.query(Cell).all()

        max_x: int
        max_y: int
        max_x, max_y = self.session.query(
            func.max(Cell.x),
            func.max(Cell.y)
        ).one()

        self.session.commit()
        print("ПРЕДЕЛЫ", max_x, max_y)
        matrix: list[list[Cell]] = [
            [None for _y in range(max_y + 1)]
            for _x in range(max_x + 1)
        ]
        for cell in cells:
            matrix[cell.x][cell.y] = cell

        return matrix

    def update_cell(self, x: int, y: int, content: str) -> None:
        cell = self.session.query(Cell).filter_by(x=x, y=y).first()
        cell.content = content
        self.session.commit()

    @staticmethod
    def create_empty_table(rows: int, columns: int) -> list[list[Cell]]:
        """
        Returns the matrix of Cell() objects with numbered rows and columns.

        Example of "numbered" matrix:
        0 1 2
        1 _ _
        2 _ _
        """
        cells = [[Cell(
            x=x,
            y=y,
            content=str(x + y) if x * y == 0 else ''
        ) for x in range(rows + 1)] for y in range(columns + 1)]
        print(cells)
        return cells
 

if __name__ == "__main__":
    db = Database(engine='sqlite:///online-calc.db')
    table = db.create_empty_table(2, 2)
    db.fill_table(table)
    print(db.parse_cells())
