import json
import tempfile
from enum import Enum
from typing import Any

from . Datatypes import Table
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
        self.temp_dir_object = tempfile.TemporaryDirectory() if temp_dir is None else None
        self.temp_dir = temp_dir if temp_dir is not None else self.temp_dir_object.name

        # this MUST be done in 2 steps because else the TemporaryDirectory() will delete itself

    def output(self) -> dict:
        return self.data

    def toJSON(self):
        data = self.convert_tables_to_json(self.data),  # Convert tables in 'data'
        serializable_data = {
            "input_file": self.input_file,
            "output_dir": self.output_dir,
            "output_filetype": self.output_filetype,
            "mode": self.mode,
            "data": data,
            "temp_dir": self.temp_dir
        }
        return json.dumps(serializable_data, sort_keys=True, indent=4)

    @classmethod
    def fromJSON(cls, json_str):
        json_data = json.loads(json_str)
        json_data = cls.convert_jsons_to_table(json_data)  # Convert tables in 'data'

        output_filetype = Filetype(json_data["output_filetype"]) if "output_filetype" in json_data else Filetype.XML
        mode = Mode(json_data["mode"]) if "mode" in json_data else Mode.PERFORMANCE
        temp_dir = json_data.get("temp_dir")

        return cls(
            data=json_data["data"][0],
            input_file=json_data["input_file"],
            output_dir=json_data["output_dir"],
            output_filetype=output_filetype,
            mode=mode,
            temp_dir=temp_dir
        )

    def convert_tables_to_json(self, data):
        # TODO: research which type of method is best practice here, classmethod, staticmethod or regular
        if type(data) == Table.Table:
            # If the current item is an instance of the Table class, convert it to JSON
            return data.to_json_with_coords()
        if isinstance(data, dict):
            # If the current item is a dictionary, recursively process its values
            return {key: self.convert_tables_to_json(value) for key, value in data.items()}
        if isinstance(data, list):
            # If the current item is a list, recursively process its elements
            return [self.convert_tables_to_json(item) for item in data]
        # If it's neither a Table nor a container, return it as is
        return data

    @classmethod
    # TODO: research which type of method is best practice here, classmethod, staticmethod or regular
    def convert_jsons_to_table(cls, data: Any) -> Any:
        if isinstance(data, str):
            try:
                table = Table.Table.from_json(data)

                # If the current item is an instance of the Table class, return
                return table
            except:
                pass
        if isinstance(data, dict):
            # If the current item is a dictionary, recursively process its values
            return {key: cls.convert_jsons_to_table(value) for key, value in data.items()}
        if isinstance(data, list):
            # If the current item is a list, recursively process its elements
            return [cls.convert_jsons_to_table(item) for item in data]
        # If it's neither a Table nor a container, return it as is
        return data


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

