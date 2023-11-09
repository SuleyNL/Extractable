from toolz import compose_left

from extractable.library import *

import extractable.PDFtoImageConvertor as PDFtoImageConvertor
import extractable.ImagePreprocessor as ImagePreprocessor
import extractable.TableDetector as TableDetector
import extractable.StructureDetector as StructureDetector
import extractable.TextExtractor as TextExtractor
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
    log_text_format: str = "%(asctime)s - %(name)s - %(levelname)s - [%(className)s] - %(message)s"  # type: ignore

    FORMATS = {
        logging.DEBUG: grey + log_text_format + reset,
        logging.INFO: green_intense + log_text_format + reset,
        logging.WARNING: yellow + log_text_format + reset,
        logging.ERROR: red + log_text_format + reset,
        logging.CRITICAL: bold_red + log_text_format + reset
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
            StructureDetector.StructureRecognitionTATR.process,
            TextExtractor.PyPDF2Textport.process,
            DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    # create a data_object which will be passed into pipeline of all classes
    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype, mode=mode)

    # run the pipeline on data_object
    pipeline(data_object)

    logger.info('Process Finished', extra={'className': 'Extractor'})


def extract_using_TATR_OCR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.INFO)

    pipeline = compose_left(
            TableDetector.TableDetectorTATR.process,
            StructureDetector.StructureRecognitionTATR.process,
            process,
            DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    # create a data_object which will be passed into pipeline of all classes
    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype, mode=mode)

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

    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype)

    pipeline(data_object)


def extract_using_TATR_structure_only(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.DEBUG)

    pipeline = compose_left(
        StructureDetector.StructureRecognitionTATR.process,
        DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype)

    pipeline(data_object)

    logger.info('Process Finished', extra={'className': 'Extractor'})


def extract_using_DETR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML):
    pipeline = compose_left(
        TableDetector.TableDetectorDETR.process,
        DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype)

    pipeline(data_object)

    
