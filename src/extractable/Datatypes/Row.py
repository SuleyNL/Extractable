import math
from typing import List

from .. Dataobj import Bbox
from . Cell import Cell
import xml.etree.ElementTree as ET


class Row:
    def __init__(
            self,
            row_id: int,
            cells: List[Cell] = None,
            xy1: tuple[float, float] = None,
            xy2: tuple[float, float] = None,
            bbox: Bbox = None  # TODO: calculate bbox from 2 tuples
    ):
        """
        :type cells: List[Cell]
        """
        self.row_id = row_id
        self.cells = cells if cells is not None else []
        self.xy1 = (round(xy1[0], 2), round(xy1[1], 2)) if xy1 is not None else tuple([round(min(cell.xy1[0] for cell in cells), 2), round(min(cell.xy1[1] for cell in cells), 2)])
        self.xy2 = (round(xy2[0], 2), round(xy2[1], 2)) if xy2 is not None else tuple([round(max(cell.xy2[0] for cell in cells), 2), round(max(cell.xy2[1] for cell in cells), 2)])

    @property
    def data(self):
        data = [cell.text for cell in self.cells]
        return data

    def to_xml_with_coords(self):
        row_element = ET.Element("tr")

        row_element.set("xy1", ", ".join(str(coord) for coord in self.xy1))
        row_element.set("xy2", ", ".join(str(coord) for coord in self.xy2))

        for cell in self.cells:
            cell_element = ET.fromstring(cell.to_xml_with_coords())
            row_element.append(cell_element)

        xml_string = ET.tostring(row_element).decode()
        return xml_string

    def add_one_cell(self, cell: Cell):
        self.cells.append(cell)
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([round(min(cell.xy1[0] for cell in self.cells), 2), round(min(cell.xy1[1] for cell in self.cells), 2)])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([round(max(cell.xy2[0] for cell in self.cells), 2), round(max(cell.xy2[1] for cell in self.cells), 2)])

    def set_cells(self, cells: List[Cell]):
        self.cells = cells
        self.xy1 = self.xy1 if self.xy1 is not None else tuple([round(min(cell.xy1[0] for cell in self.cells), 2), round(min(cell.xy1[1] for cell in self.cells), 2)])
        self.xy2 = self.xy2 if self.xy2 is not None else tuple([round(max(cell.xy2[0] for cell in self.cells), 2), round(max(cell.xy2[1] for cell in self.cells), 2)])

    def set_xy(self, xy1, xy2):
        self.xy1 = round(xy1, 2)
        self.xy2 = round(xy2, 2)

    def intersection_with_column_bbox(self, column_bbox: Bbox):
        # take the height from row
        y1 = self.xy1[1]
        y2 = self.xy2[1]

        # take width from column
        x1 = column_bbox.x1
        x2 = column_bbox.x2

        # check if the values also really are within bounds, with 2px error margin
        if math.floor(self.xy1[0])-2 <= math.floor(x1) <= math.floor(self.xy2[0])+2 \
            and \
            math.floor(self.xy1[0])-2 <= math.floor(x2) <= math.floor(self.xy2[0])+2 \
            and \
            math.floor(self.xy1[1])-2 <= math.floor(y1) <= math.floor(self.xy2[1])+2 \
            and \
            math.floor(self.xy1[1])-2 <= math.floor(y2) <= math.floor(self.xy2[1])+2:
            # return intersection area of row and column
            return Bbox(x1, y1, x2, y2)
        else:
            #TODO: RAISE OUT BOUNDS ERROR
            print('bbox error')
            return Bbox(x1, y1, x2, y2)
