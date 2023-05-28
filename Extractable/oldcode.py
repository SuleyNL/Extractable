

# Define the input and output files
data_object = DataObj({}, input_file='input.txt', output_file='output.txt')

pipes: list[Type[Pipe]] = [PDFToImageConverter, ImagePreprocessor, TableDetector, XMLConverter]


def Pipeline(dataobj: DataObj, pipes: list[Type[Pipe]]):
    # Initialize dataobj
    processed_dataobj = dataobj

    # Apply pipelines in sequence
    for pipe in pipes:
        processed_dataobj = pipe.process(processed_dataobj)

    # Return final processed data object
    return processed_dataobj.output()


# Build pipeline of desired functions and order
pipeline = compose_left(
    PDFToImageConverter.process,
    ImagePreprocessor.process,
    TableDetector.process,
    TextExtractor.process,
    XMLConverter.process,
    DataObj.output
)

# Start pipeline with desired DataObj
# print(Pipeline(data_object, pipes))
# print(pipeline(data_object))
