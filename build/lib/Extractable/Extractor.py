from toolz import compose_left

from Extractable.library import *

import Extractable.PDFtoImageConvertor as PDFtoImageConvertor
import Extractable.ImagePreprocessor as ImagePreprocessor
import Extractable.TableDetector as TableDetector
import Extractable.StructureDetector as StructureDetector
import Extractable.TextExtractor as TextExtractor
import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = "\x1b[0;32m"
    green_intense = "\x1b[0;92m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[0;94m"
    reset = "\x1b[0m"
    format = '%(asctime)s - %(name)s - %(levelname)s - [%(className)s] - %(message)s'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green_intense + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger():
    # create logger
    logger = logging.getLogger('Extractor')
    # create console handler
    console_handler = logging.StreamHandler()
    # create formatter
    formatter = CustomFormatter()
    console_handler.setFormatter(formatter)
    # add console_handler to logger so it logs to console
    logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)

    return logger


logger = setup_logger()


def Logger():
    return logger


def extract(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    extract_using_TATR(input_file, output_dir, output_filetype, mode)


def extract_using_TATR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.INFO)

    pipeline = compose_left(
            TableDetector.TableDetectorTATR.process,
            StructureDetector.StructureRecognitionWithTATR.process,
            TextExtractor.TesseractOCR.process,
            DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    # create a data_object which will be passed into pipeline of all classes
    data_object = DataObj({}, input_file=input_file, output_file=output_dir, output_filetype=output_filetype, mode=mode)

    # run the pipeline on data_object
    pipeline(data_object)

    logger.info('Process Finished', extra={'className': 'Extractor'})


def extract_using_TATR_table_only(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.DEBUG)

    pipeline = compose_left(
        TableDetector.TableDetectorTATR.process,
        DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, output_filetype=output_filetype)

    pipeline(data_object)


def extract_using_TATR_structure_only(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.DEBUG)

    pipeline = compose_left(
        StructureDetector.StructureRecognitionWithTATR.process,
        DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, output_filetype=output_filetype)

    pipeline(data_object)

    logger.info('Process Finished', extra={'className': 'Extractor'})




def extract_using_DETR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML):
    pipeline = compose_left(
        TableDetector.TableDetectorDETR.process,
        DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, output_filetype=output_filetype)

    pipeline(data_object)
