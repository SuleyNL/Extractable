import xml.etree.ElementTree as ET


class Cell:
    def __init__(
            self,
            text: str,
            cell_id: int,
            xy1: tuple,
            xy2: tuple,
    ):
        self.text = text
        self.cell_id = cell_id
        self.xy1 = xy1
        self.xy2 = xy2

    def toXML(self):
        cell_element = ET.Element("td")

        cell_element.set("xy1", ",".join(str(coord) for coord in self.xy1))
        cell_element.set("xy2", ",".join(str(coord) for coord in self.xy2))
        cell_element.text = self.text

        xml_string = ET.tostring(cell_element).decode()
        return xml_string
