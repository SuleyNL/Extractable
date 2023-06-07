from bisect import bisect

import svgwrite
from PyPDF2 import PdfReader
from pytesseract import Output

from Extractable import Extractor
from Extractable.Datatypes.Table import Table
from Extractable.Datatypes.Row import Row
from Extractable.Datatypes.Cell import Cell

from Extractable.library import *

import abc
from typing import Type, List
import ntpath
import os
from pathlib import Path
import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrFeatureExtractor
import matplotlib.pyplot as plt
from transformers import TableTransformerForObjectDetection
import numpy as np
from enum import Enum
import pytesseract
import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrFeatureExtractor
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import xml.etree.ElementTree as ET


# Find indexes of values greater than the threshold
def find_indexes_greater_than(data, threshold):
    index = bisect.bisect_right(data, threshold)
    return list(range(index, len(data)))


# Find indexes of values lower than the threshold
def find_indexes_lower_than(data, threshold):
    index = bisect.bisect_left(data, threshold)
    return list(range(index))


# Find values greater than the threshold
def find_values_greater_than(data, threshold):
    index = bisect.bisect_right(data, threshold)
    return data[index:]


# Find values lower than the threshold
def find_values_lower_than(data, threshold):
    index = bisect.bisect_left(data, threshold)
    return data[:index]


class NeedlemanWunschExtraction(Pipe):
    '''
    We process the PDF document into a sequence of
    characters each with their associated bounding box and use
    the Needleman-Wunsch algorithm to align this with the
    character sequence for the text extracted from each table
    XML
    '''

    @staticmethod
    def process(dataobj):
        # Extract text from the cells
        # Return the text as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj


class PyPDF2Textport(Pipe):
    from PyPDF2 import PdfReader
    import svgwrite

    @staticmethod
    def process(dataobj: DataObj):
        logger = Extractor.Logger()
        reader = PdfReader(dataobj.input_file)
        pages = reader.pages
        dwg = svgwrite.Drawing("testestestdeleteme.svg", profile="tiny")
        page_number: int = 0
        words: dict = {
            'x': [],
            'y': [],
            'text': [],
            'page': []
        }

        # use an svg method to get the xy-coordinate of every word-group
        def visitor_svg_text(text, cm, tm, fontDict, fontSize):
            if len(text) > -1:
                (x, y) = (tm[4], tm[5])
                x = x * (1664/595)  # translate from 72 PPI format to 200PPI format: https://i.stack.imgur.com/ti1Z7.png
                y = y * (2339/842)  # translate from 72 PPI format to 200PPI format: https://i.stack.imgur.com/ti1Z7.png
                y = 2339 - y  # translate from bottom-to-top coordinate system to top-to-bottom coordinate system

                words['x'].append(x)
                words['y'].append(y)
                words['text'].append(text)
                words['page'].append(page_number)

        for page_number, page in enumerate(pages):
            page.extract_text(visitor_text=visitor_svg_text)

        # sort words by page ascending
        words['x'], words['y'], words['text'], words['page'] = zip(
            *sorted(zip(words['x'], words['y'], words['text'], words['page']), key=lambda a: a[3]))

        table_structures: List[Table] = dataobj.data['table_structures']
        table_images: List[str] = dataobj.data['table_images']
        table_locations:  List[List] = dataobj.data['table_locations']
        table_corrections:  List[List] = dataobj.data['table_corrections']
        final_tables: List[Table] = []

        for table_nr, (table_xml, table_image_path, table_correction) in enumerate(zip(table_structures, table_images, table_corrections)):
            image = Image.open(table_image_path).convert("RGB")
            max_width = image.width
            max_height = image.height
            page_nr = table_locations[table_nr]['page']

            for row in table_xml.rows:
                for cell_nr, cell in enumerate(row.cells):
                    x_correction = table_correction[0]
                    y_correction = table_correction[1]

                    bbox_true = [
                        min(cell.xy1[0] + x_correction, max_width) if x_correction > 0 else max(cell.xy1[0] + x_correction, 0),  # true_x_min (width) +40 to undo the -40 of TableDetector
                        min(cell.xy1[1] + y_correction, max_height) if y_correction > 0 else max(cell.xy1[1] + y_correction, 0),  # true_y_min (height) +40 to undo the -40 of TableDetector
                        min(cell.xy2[0] + x_correction, max_width) if x_correction > 0 else max(cell.xy2[0] + x_correction, 0),  # true_x_max (width)
                        min(cell.xy2[1] + y_correction, max_height) if y_correction > 0 else max(cell.xy2[1] + y_correction, 0),  # true_y_max (height)
                    ]

                    x1, y1, x2, y2 = bbox_true
                    x1 += table_locations[table_nr]['x']
                    x2 += table_locations[table_nr]['x']
                    y1 += table_locations[table_nr]['y']
                    y2 += table_locations[table_nr]['y']

                    words_in_bounds = {
                        'x': [],
                        'y': [],
                        'text': [],
                        'page': []
                    }

                    for x, y, text, page in zip(words['x'], words['y'], words['text'], words['page']):
                        if page == page_nr and x1 <= x <= x2 and y1-5 <= y <= y2+5:
                            words_in_bounds['x'].append(x)
                            words_in_bounds['y'].append(y)
                            words_in_bounds['text'].append(text)
                            words_in_bounds['page'].append(page_nr)

                    cell.text = ''.join(words_in_bounds['text'])
            final_tables.append(table_xml)

            # Convert detected table structure to XML Object
            table_xml = ET.fromstring(table_xml.toXML())

            # Create an ElementTree object
            tree = ET.ElementTree(table_xml)

            # Prettify XML output
            ET.indent(tree, space="\t", level=0)

            # Write the XML object to the file
            file_prefix = os.path.splitext(dataobj.output_file)[0]

            if ntpath.isdir(file_prefix):
                output_file = file_prefix + '/' + 'table_' + str(table_nr+1) + '.xml'
            else:
                output_file = file_prefix + '_table_' + str(table_nr+1) + '.xml'

            if not Path(output_file).parent.exists():
                os.makedirs(Path(output_file).parent)

            tree.write(output_file, encoding="utf-8")

            logger.info('Full XML including text saved to: %s', output_file, extra={'className': __class__.__name__})
        dataobj.data['final_tables'] = final_tables
        return dataobj


class TesseractOCR(Pipe):
    @staticmethod
    def process(dataobj: DataObj):
        os.putenv('TESSDATA_PREFIX', 'eng.traineddata')
        os.putenv('TESSDATA_PREFIX', 'nld.traineddata')

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe' #TODO: install in PATH just like Poppler

        logger = Extractor.Logger()
        # Extract text from the cells
        # Return the text as an object that can be passed to the next step in the pipeline
        table_structures: List[Table] = dataobj.data['table_structures']
        table_images: List[str] = dataobj.data['table_images']

        for table_xml, image_path in zip(table_structures, table_images):
            image = Image.open(image_path).convert("RGB")
            max_width = image.width
            max_height = image.height
            if dataobj.mode == Mode.DEBUG:  # TODO: SHOULD BE PRESENTATION
                # plt.figure(figsize=(2, 1))
                plt.imshow(image)
                plt.axis('on')
                plt.title(' image of all cells')
                plt.show()

            for row in table_xml.rows:
                for j, cell in enumerate(row.cells):
                    # Increase the bounding box size by 5 pixels on all sides so that it captures the entire area inside
                    bbox_enlarged = [
                        max(cell.xy1[0] - 10, 0),  # expanded_x_min (width)
                        max(cell.xy1[1] - 5, 0),  # expanded_y_min (height)
                        min(cell.xy2[0] + 10, max_width),  # expanded_x_max (width)
                        min(cell.xy2[1] + 5, max_height)  # expanded_y_max (height)
                    ]
                    cell_image = image.crop(bbox_enlarged)

                    read_roi12 = pytesseract.image_to_data(cell_image, config='--psm 12 --oem 3', output_type=Output.DICT, lang='nld')
                    logger.info('12: detected text with confidence of ' + str(read_roi12['conf'][-1]) + ' containing the text: \'' + read_roi12['text'][-1] + '\'', extra={'className': __class__.__name__})

                    # TODO: 11 and 13 are great methods aswell excelling in their own ways, but 12 is the best.
                    #  Might use 11 and 13 in the future for multi-voting system. so keeping the code commented for now
                    ''' 
                    read_roi11 = pytesseract.image_to_data(cell_image, config='--psm 11 --oem 3',output_type=Output.DICT, lang='nld')
                    logger.info('11: detected text with confidence of ' + str(read_roi11['conf'][-1]) + ' containing the text: \'' + read_roi11['text'][-1] + '\'', extra={'className': __class__.__name__})

                    read_roi13 = pytesseract.image_to_data(cell_image, config='--psm 13 --oem 3', output_type=Output.DICT, lang='nld')
                    logger.info('13: detected text with confidence of ' + str(read_roi13['conf'][-1]) + ' containing the text: \'' + read_roi13['text'][-1] + '\'', extra={'className': __class__.__name__})
                    '''

                    if dataobj.mode == Mode.DEBUG: #TODO: SHOULD BE PRESENTATION
                        plt.imshow(cell_image)
                        plt.axis('on')
                        plt.title('cropped image of only cell | number ' +
                                  str(j + 1) + ' out of ' + str(len(row.cells)*len(table_xml.rows)) +
                                  'text: ' + read_roi12['text'][-1])
                        plt.show()


        dataobj.data[__class__.__name__] = {}
        return dataobj
