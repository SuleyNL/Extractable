import json
import tempfile
from enum import Enum
from . ModeManager import Mode
from . Filetype import Filetype


class DataObj:
    def __init__(self,
                 input_file: str,
                 output_dir: str,
                 output_filetype: Filetype = Filetype.XML,
                 mode: Mode = Mode.PERFORMANCE,
                 data: dict | None = None,
                 temp_dir: str | None = None):

        self.input_file = input_file    # input can be pdf or img
        self.output_dir = output_dir
        # self.output_file expects an output dir, for example 'tables/'
        # will produce files named 'tables/_table_1.xml' and 'tables/_table_2.xml' etc.
        # if not a dir, for example 'tables/hello', it will be treated as prefix
        # so it will produce 'tables/hello_table_1.xml', 'tables/hello_table_2.xml' etc.
        self.output_filetype = output_filetype
        self.mode = mode

        if data is None:
            data = {
                'pdf_images': None if input_file.endswith('.pdf') else [input_file],
                'table_locations': None,
                'table_corrections': None,
                'table_images': None,
                'table_structures': None,
                'final_tables': None}
        self.data = data

        if temp_dir is None:
            # this MUST be done in 2 steps because else the TemporaryDirectory() will delete itself
            created_dir = tempfile.TemporaryDirectory()
            self.temp_dir = created_dir.name
        else:
            self.temp_dir = temp_dir

    def output(self) -> dict:
        return self.data

    def toJSON(self):
        serializable_data = {
            "input_file": self.input_file,
            "output_file": self.output_dir,
            "output_filetype": self.output_filetype,
            "mode": self.mode,
            "data": self.data,
            "temp_dir": self.temp_dir
        }
        return json.dumps(serializable_data, sort_keys=True, indent=4)

    @classmethod
    def fromJSON(cls, json_str):
        json_data = json.loads(json_str)

        output_filetype = Filetype(json_data["output_filetype"]) if "output_filetype" in json_data else Filetype.XML
        mode = Mode(json_data["mode"]) if "mode" in json_data else Mode.PERFORMANCE
        temp_dir = json_data.get("temp_dir")

        return cls(
            data=json_data["data"],
            input_file=json_data["input_file"],
            output_dir=json_data["output_file"],
            output_filetype=output_filetype,
            mode=mode,
            temp_dir=temp_dir
        )


class Bbox:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

    @property
    def xy1(self):
        return self.x1, self.y1

    @property
    def xy2(self):
        return self.x2, self.y2

    @property
    def box(self):
        return [self.x1, self.y1, self.x2, self.y2]

    @property
    def width(self):
        return abs(self.x1 - self.x2)

    @property
    def height(self):
        return abs(self.y1 - self.y2)

    @property
    def area(self):
        """
        Calculates the surface area. useful for IOU!
        """
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)

    def intersection_area(self, bbox):
        x1 = max(self.x1, bbox.x1)
        y1 = max(self.y1, bbox.y1)
        x2 = min(self.x2, bbox.x2)
        y2 = min(self.y2, bbox.y2)
        intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
        return intersection

    def iou(self, bbox):
        intersection = self.intersection_area(bbox)

        iou = intersection / float(self.area + bbox.area - intersection)
        # return the intersection over union value
        return iou


# TODO: review Legacy code
def intersects(box1: tuple, box2: tuple,
               box1_width: int = 100, box1_height: int = 15,
               box2_width: int = 100, box2_height: int = 15):

    # accepts two tuples within which:
    # tuple[0] = x
    # tuple[1] = y

    x1, y1 = box1
    box1_top_left = (x1,            y1)
    box1_top_right = (x1 + box1_width,    y1)
    box1_bottom_left = (x1,            y1 + box1_height)
    box1_bottom_right = (x1 + box1_width,    y1 + box1_height)

    x2, y2 = box2
    box2_top_left = (x2,            y2)
    box2_top_right = (x2 + box2_width,    y2)
    box2_bottom_left = (x2,            y2 + box2_height)
    box2_bottom_right = (x2 + box2_width,    y2 + box2_height)

    return not (box1_top_right[0] < box2_bottom_left[0] or box1_bottom_left[0] > box2_top_right[0] or box1_top_right[1] > box2_bottom_left[1] or box1_bottom_left[1] < box2_top_right[1])

