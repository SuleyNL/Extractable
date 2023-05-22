from typing import List
from Extractable.Datatypes.Cell import Cell
import xml.etree.ElementTree as ET


class Row:
    def __init__(
            self,
            cells: List[Cell],
            row_id: int,
            xy1: tuple = None,
            xy2: tuple = None
    ):
        self.cells = cells
        self.row_id = row_id
        self.xy1 = xy1 if xy1 is not None else tuple([min(cell.xy1[0] for cell in cells), min(cell.xy1[1] for cell in cells)])
        self.xy2 = xy2 if xy2 is not None else tuple([max(cell.xy2[0] for cell in cells), max(cell.xy2[1] for cell in cells)])

    def toXML(self):
        row_element = ET.Element("tr")

        row_element.set("xy1", ",".join(str(coord) for coord in self.xy1))
        row_element.set("xy2", ",".join(str(coord) for coord in self.xy2))

        for cell in self.cells:
            cell_element = ET.fromstring(cell.toXML())
            row_element.append(cell_element)

        xml_string = ET.tostring(row_element).decode()
        return xml_string

    def add_one_cell(self, cell: Cell):
        self.cells.append(cell)
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([min(cell.xy1[0] for cell in self.cells), min(cell.xy1[1] for cell in self.cells)])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([max(cell.xy2[0] for cell in self.cells), max(cell.xy2[1] for cell in self.cells)])

    def set_cells(self, cells: List[Cell]):
        self.cells = cells
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([min(cell.xy1[0] for cell in self.cells), min(cell.xy1[1] for cell in self.cells)])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([max(cell.xy2[0] for cell in self.cells), max(cell.xy2[1] for cell in self.cells)])
