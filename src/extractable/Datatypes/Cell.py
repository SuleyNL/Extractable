import xml.etree.ElementTree as ET


class Cell:
    def __init__(
            self,
            text: str,
            cell_id: int,
            xy1: tuple[float, float],
            xy2: tuple[float, float],
    ):
        self.text = text
        self.cell_id = cell_id
        self.xy1 = tuple([round(min(xy1[0], xy2[0]), 2), round(min(xy1[1], xy2[1]), 2)])  # make tuple of the lowest x and y value
        self.xy2 = tuple([round(max(xy1[0], xy2[0]), 2), round(max(xy1[1], xy2[1]), 2)])  # make tuple of the highest x and y value

    def to_xml_with_coords(self):
        cell_element = ET.Element("td")

        cell_element.set("xy1", ", ".join(str(coord) for coord in self.xy1))
        cell_element.set("xy2", ", ".join(str(coord) for coord in self.xy2))
        cell_element.text = self.text

        xml_string = ET.tostring(cell_element).decode()
        return xml_string

    def set_xy(self, xy1, xy2):
        self.xy1 = round(xy1, 2)
        self.xy2 = round(xy2, 2)
