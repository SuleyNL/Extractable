import ntpath
import os
import platform
from pathlib import Path

from Extractable.Pipe import Pipe
from Extractable.Dataobj import DataObj

from Extractable import Logger
from Extractable import ModeManager

import pdf2image
from pdf2jpg import pdf2jpg


class ConvertUsingPDF2image(Pipe):
    @staticmethod
    def process(dataobj: DataObj) -> DataObj:
        # Convert the PDF to an image using pdf2image library (has dependency on poppler)
        # Return the image as an object that can be passed to the next step in the pipeline
        logger = Logger.Logger()

        poppler_path = ConvertUsingPDF2image.install_poppler()

        images = pdf2image.convert_from_path(dataobj.input_file, poppler_path=poppler_path)
        path_to_images = []

        for i, image in enumerate(images):
            # Save image into temporary directory
            image_path = ConvertUsingPDF2image.save_img_to_temp(dataobj, logger, image, i, path_to_images)

            # Send image and mode to ModeManager to potentially display it
            ModeManager.PDFtoImageConvertor_display_image(dataobj.mode, image_path,  i, len(images))

        dataobj.data['pdf_images'] = path_to_images
        dataobj.data[__class__.__name__] = {}
        return dataobj

    @staticmethod
    def install_poppler():
        poppler_path = None

        if platform.system() == "Windows":
            poppler_path = os.path.join(os.path.dirname(__file__), 'poppler-0.68.0(win)', 'bin')

        elif platform.system() == "Linux":
            poppler_path = os.path.join(os.path.dirname(__file__), 'poppler-23.06.0(linux)')

        return poppler_path

    @staticmethod
    def save_img_to_temp(dataobj, logger, image, i, path_to_images):
        image_name = Path(ntpath.basename(dataobj.input_file)).stem
        image_path_string = f"{image_name}_page_{i + 1}.jpg"
        image_path = dataobj.temp_dir + '\\' + os.path.normpath(image_path_string)
        logger.info('Saved image to: ' + image_path, extra={'className': __class__.__name__})

        image.save(image_path, "JPEG")
        path_to_images.append(image_path)

        return image_path


# space for other conversion methods. this one is not in use
class dont_use_ConvertUsingPDF2JPG(Pipe):
    @staticmethod
    def process(dataobj: DataObj) -> DataObj:
        # This class doesn't work (yet) !
        # Convert the PDF to an image using pdf2jpg library dependent (uses cmd commands under the hood)
        # Return the image as an object that can be passed to the next step in the pipeline

        output_dir = 'tables/'

        result = pdf2jpg.convert_pdf2jpg(dataobj.input_file, output_dir, pages="ALL")

        dataobj.data[__class__.__name__] = {}
        return dataobj
