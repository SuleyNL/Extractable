from toolz import compose_left
import Extractable.library as l

data_object = l.DataObj({}, input_file='input.txt', output_file='output.txt')

extract_using_test = compose_left(
        l.PDFToImageConverter.process,
        l.ImagePreprocessor.process,
        l.TableDetector.process,
        l.TextExtractor.process,
        l.XMLConverter.process,
        l.DataObj.output
    )


def extract_using_TATR(input_file: str, output_dir: str):
    pipeline = compose_left(
        #l.TableDetectorTATR.process,
        l.TableStructureDetectorTATR.process,
        l.DataObj.output)

    data_object = l.DataObj({}, input_file=input_file, output_file=output_dir)

    output = pipeline(data_object)

    print(output)

    #print(e.pipes)
    #print("true")


def extract_using_Alg1(inputfile:str, outputdir:str):
    #print(l.pipes)
    print("true")
