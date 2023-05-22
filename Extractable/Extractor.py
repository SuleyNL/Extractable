from toolz import compose_left

from Extractable import *
import Extractable.library as l
from Extractable import PDFtoImageConvertor
from Extractable import ImagePreprocessor
from Extractable import TableDetector
from Extractable import StructureDetector
from Extractable import TextExtractor


data_object = l.DataObj({}, input_file='input.txt', output_file='output.txt')

extract_using_test = compose_left(
        PDFtoImageConvertor.ConvertUsingPDF2image.process,
        ImagePreprocessor.StandardPreprocessor.process,
        TableDetector.TableDetectorTATR.process,
        TextExtractor.TextExtractorTesseractOCR.process,
        l.DataObj.output
    )


def extract_using_TATR_table_only_from_img(input_file: str, output_dir: str):
    pipeline = compose_left(
        TableDetector.TableDetectorTATR.process,
        l.DataObj.output)

    data_object = l.DataObj({}, input_file=input_file, output_file=output_dir)

    output = pipeline(data_object)

    print(output)


def extract_using_TATR_table_only_from_PDF(input_file: str, output_dir: str):
    pipeline = compose_left(
        PDFtoImageConvertor.ConvertUsingPDF2image.process,
        TableDetector.TableDetectorTATR.process,
        l.DataObj.output)

    data_object = l.DataObj({}, input_file=input_file, output_file=output_dir)

    output = pipeline(data_object)

    print(output)


def extract_using_TATR_structure_only(input_file: str, output_dir: str):
    pipeline = compose_left(
        PDFtoImageConvertor.ConvertUsingPDF2image.process,
        StructureDetector.StructureRecognitionWithTATR.process,
        l.DataObj.output)

    data_object = l.DataObj({}, input_file=input_file, output_file=output_dir)

    output = pipeline(data_object)

    print(output)


def extract_using_TATR(input_file: str, output_dir: str):
    pipeline = compose_left(
        PDFtoImageConvertor.ConvertUsingPDF2image.process,
        TableDetector.TableDetectorTATR.process,
        StructureDetector.StructureRecognitionWithTATR.process,
        l.DataObj.output)

    data_object = l.DataObj({}, input_file=input_file, output_file=output_dir)

    output = pipeline(data_object)

    print(output)


def extract_using_DETR(input_file: str, output_dir: str):
    pipeline = compose_left(
        TableDetector.TableDetectorDETR.process,
        l.DataObj.output)

    data_object = l.DataObj({}, input_file=input_file, output_file=output_dir)

    output = pipeline(data_object)

    print(output)


def extract_using_ALL(input_file: str, output_dir: str):
    pipeline = compose_left(
        l.TableDetectorDETR.process,
        l.TableDetectorTATR.process,
        l.DataObj.output)

    data_object = l.DataObj({}, input_file=input_file, output_file=output_dir)

    output = pipeline(data_object)

    print(output)


def extract_using_Alg1(inputfile:str, outputdir:str):
    #print(l.pipes)
    print("true")
