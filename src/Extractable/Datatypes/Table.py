from typing import List
from Extractable.Datatypes.Row import Row
import xml.etree.ElementTree as ET


class Table:
    def __init__(
            self,
            table_id,
            rows: List[Row],
            xy1: tuple = None,
            xy2: tuple = None
    ):
        self.table_id = table_id
        self.rows = rows
        self.xy1 = xy1 if xy1 is not None else tuple([min(row.xy1[0] for row in rows), min(row.xy1[1] for row in rows)])
        self.xy2 = xy2 if xy2 is not None else tuple([max(row.xy2[0] for row in rows), max(row.xy2[1] for row in rows)])

    def toXML(self):
        # Create an XML object
        table_element = ET.Element("tabular")

        table_element.set("xy1", ",".join(str(coord) for coord in self.xy1))
        table_element.set("xy2", ",".join(str(coord) for coord in self.xy2))

        for row in self.rows:
            row_element = ET.fromstring(row.toXML())
            table_element.append(row_element)

        xml_string = ET.tostring(table_element).decode()
        return xml_string

    def add_one_row(self, row: Row):
        self.rows.append(row)
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([min(row.xy1[0] for row in self.rows), min(row.xy1[1] for row in self.rows)])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([max(row.xy2[0] for row in self.rows), max(row.xy2[1] for row in self.rows)])

    def set_rows(self, rows: List[Row]):
        self.rows = rows
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([min(row.xy1[0] for row in self.rows), min(row.xy1[1] for row in self.rows)])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([max(row.xy2[0] for row in self.rows), max(row.xy2[1] for row in self.rows)])
