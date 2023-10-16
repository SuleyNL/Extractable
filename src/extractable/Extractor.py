import logging
from toolz import compose_left

from src.extractable import PDFtoImageConvertor, StructureDetector, TableDetector, TextExtractor, Logger
from src.extractable.Dataobj import DataObj
from src.extractable.Filetype import Filetype
from src.extractable.ModeManager import Mode

logger = Logger.Logger()


def extract(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    return extract_using_TATR(input_file, output_dir, output_filetype, mode)


def extract_using_TATR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.INFO)

    pipeline = compose_left(
            TableDetector.TableDetectorTATR.process,
            StructureDetector.StructureRecognitionWithTATR.process,
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

    return data_object


def extract_using_TATR_OCR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
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
    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype, mode=mode)

    # run the pipeline on data_object
    pipeline(data_object)

    logger.info('Process Finished', extra={'className': 'Extractor'})
    return data_object


def extract_using_TATR_table_only(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.DEBUG)

    pipeline = compose_left(
        TableDetector.TableDetectorTATR.process,
        DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype, mode=mode)

    pipeline(data_object)

    return data_object


def extract_using_TATR_structure_only(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML, mode:Mode = Mode.PERFORMANCE):
    if mode == Mode.DEBUG:
        logger.setLevel(logging.DEBUG)

    pipeline = compose_left(
        StructureDetector.StructureRecognitionWithTATR.process,
        DataObj.output)

    if input_file.endswith('.pdf'):
        pipeline = compose_left(PDFtoImageConvertor.ConvertUsingPDF2image.process,
                                pipeline)

    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype, mode=mode)

    pipeline(data_object)

    logger.info('Process Finished', extra={'className': 'Extractor'})
    return data_object


def extract_using_DETR(input_file: str, output_dir: str, output_filetype: Filetype = Filetype.XML):
    # This is only included as an example of how other Machine Learning algorithms could be used, DETR is
    # not a Model trained on Table Detection
    pipeline = compose_left(
        TableDetector.TableDetectorDETR.process,
        DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_dir=output_dir, output_filetype=output_filetype)

    pipeline(data_object)

