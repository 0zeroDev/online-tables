from models import Base, Cell
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, engine: str) -> None:
        self.engine = create_engine(engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        Base.metadata.create_all(self.engine)

    def fill_table(self, table: list[list[Cell]]) -> None:
        try:
            with self.session.begin() as session:
                for row in table:
                    session.add_all(row)
        except IntegrityError as e:
            print("Objects alredy exists...", e)

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

    def parse_cells(self) -> list[list[Cell]]:
        """
        Returns matrix of cells parsed from cells table.
        """
        with self.session.begin() as session:
            cells: list[Cell] = session.query(Cell).all()

            max_x: int
            max_y: int
            max_x, max_y = session.query(
                func.max(Cell.x),
                func.max(Cell.y)
            ).one()

        matrix: list[list[Cell]] = [
            [None for _ in range(max_y + 1)]
            for _ in range(max_x + 1)
        ]
        for cell in cells:
            matrix[cell.x][cell.y] = cell

        return matrix


if __name__ == "__main__":
    db = Database(engine='sqlite:///online-calc.db')
    table = db.create_empty_table(2, 2)
    db.fill_table(table)
    print(db.parse_cells())
    
