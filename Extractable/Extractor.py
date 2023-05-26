from toolz import compose_left

from Extractable import *
from Extractable.library import *
from Extractable import PDFtoImageConvertor
from Extractable import ImagePreprocessor
from Extractable import TableDetector
from Extractable import StructureDetector
from Extractable import TextExtractor
import logging


# create logger
logger = logging.getLogger('Extractor')
# create console handler
console_handler = logging.StreamHandler()
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(className)s] - %(message)s')
console_handler.setFormatter(formatter)
# add console_handler to logger so it logs to console
logger.addHandler(console_handler)


def Logger():
    return logger


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


def extract_using_TATR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.DEBUG)

    pipeline = compose_left(
            TableDetector.TableDetectorTATR.process,
            StructureDetector.StructureRecognitionWithTATR.process,
            DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    # create a data_object which will be passed into pipeline of all classes
    data_object = DataObj({}, input_file=input_file, output_file=output_dir, output_filetype=output_filetype, mode=mode)

    # run the pipeline on data_object
    pipeline(data_object)

    logger.info('Process Finished', extra={'className': 'Extractor'})


def extract_using_DETR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML):
    pipeline = compose_left(
        TableDetector.TableDetectorDETR.process,
        DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, output_filetype=output_filetype)

    pipeline(data_object)
