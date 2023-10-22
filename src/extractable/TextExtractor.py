import math
import platform

import svgwrite
from PyPDF2 import PdfReader
from pytesseract import Output

from src.extractable import Extractor
from src.extractable import Logger, ModeManager
from src.extractable.Pipe import Pipe
from src.extractable.Dataobj import DataObj
from src.extractable.Filetype import Filetype

from src.extractable.Datatypes.Table import Table

from typing import List
import ntpath
import os
from pathlib import Path

import pytesseract

from PIL import Image

import xml.etree.ElementTree as ET


class PyPDF2Textport(Pipe):
    from PyPDF2 import PdfReader
    import svgwrite

    @staticmethod
    def process(dataobj: DataObj) -> DataObj:
        logger = Logger.Logger()

        words = PyPDF2Textport.extractText(dataobj)

        table_structures: List[Table] = dataobj.data['table_structures']
        table_images: List[str] = dataobj.data['table_images']
        table_locations: List[List] = dataobj.data['table_locations']
        table_corrections: List[List] = dataobj.data['table_corrections']
        final_tables: List[Table] = []

        if len(table_locations) == 0:
            # no tables detected to run structure detector on
            return dataobj

        # Loop past each Table object to check if cell bounding boxes correlate to text bounding boxes
        for table_nr, (table, table_image_path, table_correction) in enumerate(
                zip(table_structures, table_images, table_corrections)):
            # get the page_nr where this Table object is detected
            page_nr = table_locations[table_nr]['page']
            for row in table.rows:
                for cell_nr, cell in enumerate(row.cells):
                    '''
                    # Correction for table location is now done inside StructureDetector instead of here
                    # Leaving the code still here but commented out just in case it is useful to revert
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
                    '''
                    (x1, y1), (x2, y2) = (cell.xy1, cell.xy2)

                    words_in_bounds = {
                        'x': [],
                        'y': [],
                        'text': [],
                        'page': []
                    }

                    for x, y, text, font_size, page in zip(words['x'], words['y'], words['text'], words['font_size'],
                                                           words['page']):
                        # Loop through the words to see if they are inside the boundaries of current Cell object,
                        # if yes, add to cell.text
                        padding = math.ceil(font_size)
                        if page == page_nr and x1 - padding <= x <= x2 + padding and y1 + padding <= y <= y2 + padding:
                            words_in_bounds['x'].append(x)
                            words_in_bounds['y'].append(y)
                            words_in_bounds['text'].append(text)
                            words_in_bounds['page'].append(page_nr)

                    cell.text = ''.join(words_in_bounds['text'])
            final_tables.append(table)

            # TODO: TextExtractor.output_table

            # Convert detected table structure to XML Object
            table_xml = ET.fromstring(table.to_xml_with_coords())

            # Create an ElementTree object
            tree = ET.ElementTree(table_xml)

            # Prettify XML output
            ET.indent(tree, space="\t", level=0)

            # Write the XML object to the file
            file_prefix = os.path.splitext(dataobj.output_file)[0]

            if ntpath.isdir(file_prefix):
                output_file = file_prefix + '/' + 'table_' + str(table_nr + 1)
            else:
                output_file = file_prefix + '_table_' + str(table_nr + 1)

            if not Path(output_file).parent.exists():
                os.makedirs(Path(output_file).parent)

            if dataobj.output_filetype == Filetype.XML:
                tree.write(output_file + '.xml', encoding="utf-8")

            if dataobj.output_filetype == Filetype.CSV:
                table.to_csv(output_file)

            if dataobj.output_filetype == Filetype.JSON:
                table.to_json(output_file)

            if dataobj.output_filetype == Filetype.PARQUET:
                table.to_parquet(output_file)

            if dataobj.output_filetype == Filetype.LATEX:
                table.to_latex(output_file)

            if dataobj.output_filetype == Filetype.EXCEL:
                table.to_excel(output_file)

            logger.info('Full XML including text saved to: %s', output_file, extra={'className': __class__.__name__})
        dataobj.data['final_tables'] = final_tables
        return dataobj

    @staticmethod
    def extractText(dataobj: DataObj) -> DataObj:
        # GET ALL WORDS FROM ALL PAGES
        # TODO: can be done more efficiently, only certain pages

        reader = PdfReader(dataobj.input_file)

        pages = reader.pages
        dwg = svgwrite.Drawing("testestestdeleteme.svg", profile="tiny")
        page_number: int = 0
        words: dict = {
            'x': [],
            'y': [],
            'text': [],
            'font_size': [],
            'page': []
        }

        # use an svg method to get the xy-coordinate of every word-group
        def visitor_svg_text(text, cm, tm, fontDict, fontSize):
            if len(text) > -1:
                (x, y) = (tm[4], tm[5])
                x = x * (
                        1664 / 595)  # translate from 72 PPI format to 200PPI format: https://i.stack.imgur.com/ti1Z7.png
                y = y * (
                        2339 / 842)  # translate from 72 PPI format to 200PPI format: https://i.stack.imgur.com/ti1Z7.png
                y = 2339 - y  # translate from bottom-to-top coordinate system to top-to-bottom coordinate system

                words['x'].append(x)
                words['y'].append(y)
                words['text'].append(text)
                words['font_size'].append(fontSize)
                words['page'].append(page_number)

        for page_number, page in enumerate(pages):
            page.extract_text(visitor_text=visitor_svg_text)

        # sort words by page ascending
        words['x'], words['y'], words['text'], words['font_size'], words['page'] = zip(
            *sorted(zip(words['x'], words['y'], words['text'], words['font_size'], words['page']), key=lambda a: a[3]))

        return words


class TesseractOCR(Pipe):
    '''
    This code doesnt work yet. It still should be built out further
    '''
    path_to_tesseract = None

    @staticmethod
    def process(dataobj: DataObj) -> DataObj:
        TesseractOCR.download_tesseract()
        os.putenv('TESSDATA_PREFIX', 'eng.traineddata')
        os.putenv('TESSDATA_PREFIX', 'nld.traineddata')

        pytesseract.pytesseract.tesseract_cmd = TesseractOCR.path_to_tesseract

        logger = Extractor.Logger()
        # Extract text from the cells
        # Return the text as an object that can be passed to the next step in the pipeline
        table_structures: List[Table] = dataobj.data['table_structures']
        table_images: List[str] = dataobj.data['table_images']

        for table_xml, image_path in zip(table_structures, table_images):
            image = Image.open(image_path).convert("RGB")
            max_width = image.width
            max_height = image.height

            ModeManager.TextExtractor_display_table(dataobj.mode, image)

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

                    read_roi12 = pytesseract.image_to_data(cell_image, config='--psm 12 --oem 3',
                                                           output_type=Output.DICT,
                                                           lang='nld')
                    logger.info(
                        '12: detected text with confidence of ' + str(
                            read_roi12['conf'][-1]) + ' containing the text: \'' +
                        read_roi12['text'][-1] + '\'', extra={'className': __class__.__name__})

                    # TODO: 11 and 13 are great methods as well excelling in their own ways, but 12 is the best.
                    #  Might use 11 and 13 in the future for multi-voting system. so keeping the code commented for now
                    ''' 
                    read_roi11 = pytesseract.image_to_data(cell_image, config='--psm 11 --oem 3',output_type=Output.DICT, lang='nld')
                    logger.info('11: detected text with confidence of ' + str(read_roi11['conf'][-1]) + ' containing the text: \'' + read_roi11['text'][-1] + '\'', extra={'className': __class__.__name__})

                    read_roi13 = pytesseract.image_to_data(cell_image, config='--psm 13 --oem 3', output_type=Output.DICT, lang='nld')
                    logger.info('13: detected text with confidence of ' + str(read_roi13['conf'][-1]) + ' containing the text: \'' + read_roi13['text'][-1] + '\'', extra={'className': __class__.__name__})
                    '''

                    ModeManager.TextExtractor_display_cell(dataobj.mode, cell_image, row, table_xml, read_roi12)

        dataobj.data[__class__.__name__] = {}
        return dataobj

    @staticmethod
    def download_tesseract():
        import os
        import requests
        import subprocess
        logger = Extractor.Logger()

        current_os = platform.system()

        logger.info(
            'Detected ' + current_os + ' as current OS',
            extra={'className': __class__.__name__})

        if platform.system() == "Windows":
            # URL of the file to download
            url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe"

            # Name of the downloaded file
            file_name = "tesseract-ocr-w64-setup-5.3.1.20230401.exe"

            # Folder path to save the downloaded file and unpacked contents
            folder_path = os.path.join(os.path.dirname(__file__), "Tesseract-OCR")

            # File path to save the downloaded file
            file_exe_path = os.path.join(folder_path, file_name)

            # Create the folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)

            # Download the file
            logger.info(
                'Downloading Tesseract-OCR, this should take less than 1 minute...',
                extra={'className': __class__.__name__})

            response = requests.get(url)
            response.raise_for_status()
            # Save the file to the desired location
            with open(file_exe_path, "wb") as file:
                file.write(response.content)
            print("File downloaded and saved successfully!")

            # Unpack the file
            print("Unpacking Tesseract-OCR..")
            print("Please unpack Tesseract-OCR in: " + folder_path)
            unpack_folder = folder_path
            # Create the folder for the unpacked contents
            os.makedirs(unpack_folder, exist_ok=True)
            # Execute the .exe file to unpack its contents
            subprocess.run(file_exe_path, cwd=unpack_folder)
            # subprocess.run([file_exe_path, "-o" + unpack_folder])
            print("File unpacked successfully!")

            TesseractOCR.path_to_tesseract = os.path.join(os.path.dirname(__file__), unpack_folder, 'tesseract.exe')

        elif platform.system() == "Linux":
            pass

        elif platform.system() == "MacOS":
            pass


class NeedlemanWunschExtraction(Pipe):
    '''
    We process the PDF document into a sequence of
    characters each with their associated bounding box and use
    the Needleman-Wunsch algorithm to align this with the
    character sequence for the text extracted from each table
    XML
    '''

    @staticmethod
    def process(dataobj: DataObj) -> DataObj:
        # Extract text from the cells
        # Return the text as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj


