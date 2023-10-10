import tempfile
from enum import Enum
from src.Extractable.ModeManager import Mode


class Filetype(Enum):
    EXCEL = 'xlsx'
    LATEX = 'tex'
    PARQUET = 'parquet'
    PDF = 'pdf'
    IMG = 'img'
    XML = 'xml'
    JSON = 'json'
    CSV = 'csv'
    HTML = 'html'
    YAML = 'yaml'


class DataObj:
    def __init__(self, data: dict,
                 input_file: str,
                 output_dir: str,
                 output_filetype: Filetype = Filetype.XML,
                 mode: Mode = Mode.PERFORMANCE):

        data['pdf_images'] = None if input_file.endswith('.pdf') else [input_file]       # image of each page in pdf
        data['table_locations'] = None                                                   # a list of dicts, each sublist containing the leftupper x,y value of the table-cropped image, aswell as the page it belongs to and table_id
        data['table_corrections'] = None                                                 # for each table, the difference between detected table (topleft xy tuple) by TableDetector vs by StructureDetector, so this can be used to find true location of words on page
        data['table_images'] = None                                                      # image of each table
        data['table_structures'] = None                                                  # a Table() containing bboxes, for each table
        data['final_tables'] = None                                                      # a Table() containing bboxes and text, for each table

        self.data = data
        self.input_file = input_file    # input pdf or img
        self.output_file = output_dir  # output dir for example 'tables/' produces tables/_table_1.xml
                                        # if not a dir, like 'tables/hello', it will be treated as prefix
                                        # so it will produce tables/hello_table_1.xml
        self.output_filetype = output_filetype
        self.mode = mode
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = self.temp.name

    def output(self) -> dict:
        return self.data


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

