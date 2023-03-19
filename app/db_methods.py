from contextlib import contextmanager
from typing import List
from models import Base, Cell
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, engine: str) -> None:
        self.engine = create_engine(engine)
        self.Session = sessionmaker(bind=self.engine)

    def fill_table(self, table: List[List[Cell]]) -> None:
        """Create the table in the database if not exist and insert given data."""
        Base.metadata.create_all(self.engine)

        with self.get_session() as session:
            try:
                for row in table:
                    session.add_all(row)
                session.commit()
            except IntegrityError as error_message:
                print("Objects already exist.\n", error_message)

    def parse_cells(self) -> List[List[Cell]]:
        """Return a matrix of cells from database."""
        with self.get_session() as session:
            cells: List[Cell] = session.query(Cell).all()

            max_x: int
            max_y: int
            max_x, max_y = session.query(
                func.max(Cell.x),
                func.max(Cell.y)
            ).one()

            matrix: List[List[Cell]] = [
                [None for _ in range(max_y + 1)]
                for _ in range(max_x + 1)
            ]
            for cell in cells:
                matrix[cell.x][cell.y] = cell

            return matrix

    def update_cell(self, x: int, y: int, content: str) -> None:
        """Update content of the cell in the database by given coordinates"""
        with self.get_session() as session:
            cell = session.query(Cell).filter_by(x=x, y=y).first()
            if cell:
                cell.content = content
                session.commit()
            else:
                raise ValueError(f"Cell ({x}, {y}) does not exist.")

    @staticmethod
    def create_empty_table(rows: int, columns: int) -> list[list[Cell]]:
        """
        Return the matrix of Cell() objects with numbered rows and columns.

        Example of "numbered" matrix:
        0 1 2
        1 _ _
        2 _ _
        """
        cells = [[Cell(
            x=x,
            y=y,
            content=str(x + y) if x * y == 0 else ''
        )
            for x in range(rows + 1)]
            for y in range(columns + 1)]

        return cells

    @contextmanager
    def get_session(self):
        """Provide interface for transactions"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()


if __name__ == "__main__":
    db = Database(engine='sqlite:///online-calc.db')
    table = db.create_empty_table(2, 2)
    db.fill_table(table)
    print(db.parse_cells())
