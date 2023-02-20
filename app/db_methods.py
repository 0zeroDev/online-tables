from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Cell


class Database:
    def __init__(self, engine: str) -> None:
        self.engine = create_engine(engine)
        Base.metadata.create_all(self.engine)

    def fill_table(self, data: list[Cell]) -> None:
        with Session(bind=self.engine) as session:
            session.add_all(data)
            session.commit()

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

        return cells

    def parse_cells(self):  # -> list[list[Cell]]
        pass


if __name__ == "__main__":
    db = Database(engine='sqlite:///online-calc.db')
    table = db.create_empty_table(2, 2)
    for raw in table:
        db.fill_table(raw)
