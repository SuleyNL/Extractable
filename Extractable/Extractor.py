from toolz import compose_left

from Extractable import *
from Extractable.library import *
from Extractable import PDFtoImageConvertor
from Extractable import ImagePreprocessor
from Extractable import TableDetector
from Extractable import StructureDetector
from Extractable import TextExtractor


data_object = DataObj({}, input_file='input.txt', output_file='output.txt')

extract_using_test = compose_left(
        PDFtoImageConvertor.ConvertUsingPDF2image.process,
        ImagePreprocessor.StandardPreprocessor.process,
        TableDetector.TableDetectorTATR.process,
        TextExtractor.TextExtractorTesseractOCR.process,
        DataObj.output
    )


def extract_using_TATR_table_only(input_file: str, output_dir: str, filetype: Filetype = Filetype.PDF):
    if filetype == Filetype.PDF:
        pipeline = compose_left(
            PDFtoImageConvertor.ConvertUsingPDF2image.process,
            TableDetector.TableDetectorTATR.process,
            DataObj.output)
    else:
        pipeline = compose_left(
            TableDetector.TableDetectorTATR.process,
            DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, input_filetype=filetype)

    output = pipeline(data_object)

    print(output)


def extract_using_TATR_structure_only(input_file: str, output_dir: str, filetype: Filetype = Filetype.PDF):
    if filetype == Filetype.PDF:
        pipeline = compose_left(
            PDFtoImageConvertor.ConvertUsingPDF2image.process,
            StructureDetector.StructureRecognitionWithTATR.process,
            DataObj.output)
    else:
        pipeline = compose_left(
            StructureDetector.StructureRecognitionWithTATR.process,
            DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, input_filetype=filetype)

    output = pipeline(data_object)

    print(output)


def extract_using_TATR(input_file: str, output_dir: str, filetype: Filetype = Filetype.PDF):
    if filetype == Filetype.PDF:
        pipeline = compose_left(
            PDFtoImageConvertor.ConvertUsingPDF2image.process,
            TableDetector.TableDetectorTATR.process,
            StructureDetector.StructureRecognitionWithTATR.process,
            DataObj.output)
    else:
        pipeline = compose_left(
            TableDetector.TableDetectorTATR.process,
            StructureDetector.StructureReqcognitionWithTATR.process,
            DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, input_filetype=filetype)

    output = pipeline(data_object)

    print(output)


def extract_using_DETR(input_file: str, output_dir: str, filetype: Filetype = Filetype.PDF):
    pipeline = compose_left(
        TableDetector.TableDetectorDETR.process,
        DataObj.output)

    data_object = DataObj({}, input_file=input_file, output_file=output_dir, input_filetype=filetype)

    output = pipeline(data_object)

    print(output)
