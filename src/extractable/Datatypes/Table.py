from typing import List
from src.extractable.Datatypes.Row import Row
import xml.etree.ElementTree as ET
import pandas as pd


class Table:
    def __init__(
            self,
            table_id,
            rows: List[Row],
            xy1: tuple[float, float] = None,
            xy2: tuple[float, float] = None,
    ):
        self.table_id = table_id
        self.rows = rows
        self.xy1 = (round(xy1[0], 2), round(xy1[1], 2)) if xy1 is not None else tuple([round(min(row.xy1[0] for row in rows), 2), round(min(row.xy1[1] for row in rows), 2)])
        self.xy2 = (round(xy2[0], 2), round(xy2[1], 2)) if xy2 is not None else tuple([round(max(row.xy2[0] for row in rows), 2), round(max(row.xy2[1] for row in rows), 2)])

    @property
    def data(self):
        data = [row.data for row in self.rows]
        return data

    def to_xml_with_coords(self) -> str:
        # Create an XML object
        table_element = ET.Element("tabular")

        table_element.set("xy1", ",".join(str(coord) for coord in self.xy1))
        table_element.set("xy2", ",".join(str(coord) for coord in self.xy2))

        for row in self.rows:
            row_element = ET.fromstring(row.to_xml_with_coords())
            table_element.append(row_element)

        xml_string = ET.tostring(table_element).decode()
        return xml_string

    def add_one_row(self, row: Row):
        self.rows.append(row)
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([round(min(row.xy1[0] for row in self.rows)), round(min(row.xy1[1] for row in self.rows))])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([round(max(row.xy2[0] for row in self.rows)), round(max(row.xy2[1] for row in self.rows))])

    def set_rows(self, rows: List[Row]):
        self.rows = rows
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([round(min(row.xy1[0] for row in self.rows)), round(min(row.xy1[1] for row in self.rows))])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([round(max(row.xy2[0] for row in self.rows)), round(max(row.xy2[1] for row in self.rows))])

    def set_xy(self, xy1, xy2):
        self.xy1 = round(xy1, 2)
        self.xy2 = round(xy2, 2)

    def to_excel(self, file_path):
        df = pd.DataFrame(self.data)
        df.to_excel(file_path + '.xlsx', header=False, index=False)

    def to_csv(self, file_path, column_delimiter: str = ',', line_separator: str = '\r\n'):
        df = pd.DataFrame(self.data)
        df.to_csv(file_path + '.csv', header=False, index=False, sep=column_delimiter, lineterminator=line_separator)

    def to_json(self, file_path):
        df = pd.DataFrame(self.data)
        df.to_json(file_path + '.json', header=False, index=False)

    def to_sql(self, file_path, connection, table_name):
        # TODO: under construction
        df = pd.DataFrame(self.data)
        df.to_sql(name=table_name, con=connection, index=False)

    def to_latex(self, file_path):
        # TODO: not yet tested
        df = pd.DataFrame(self.data)
        df.to_latex(file_path + '.tex', header=False, index=False)

    def to_parquet(self, file_path):
        # TODO: not yet tested
        df = pd.DataFrame(self.data)
        df.to_parquet(file_path + '.parquet', header=False, index=False)
