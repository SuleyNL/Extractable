import ntpath
import os
import platform
import subprocess

import requests
import zipfile
from pathlib import Path

from . Pipe import Pipe
from . Dataobj import DataObj
from . import Logger, ModeManager

import pdf2image
from pdf2jpg import pdf2jpg
from pathlib import Path


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
        dataobj.data[__class__.__name__] = []
        return dataobj

    @staticmethod
    def install_poppler():
        poppler_path = None

        if platform.system() == "Windows":
            # Define the URL to the Poppler Windows binary
            poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0-0/Release-23.08.0-0.zip"

            # Define the path to your project directory
            location = Path(__file__).parent / 'poppler_windows'

            # Create the directory if it doesn't exist
            os.makedirs(location, exist_ok=True)

            # Define the path where you want to save the downloaded file
            downloaded_file = os.path.join(location, "poppler.zip")

            # Download the Poppler binary
            response = requests.get(poppler_url)
            with open(downloaded_file, 'wb') as f:
                f.write(response.content)

            # Extract the downloaded file
            with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
                zip_ref.extractall(location)

            poppler_path = os.path.join(os.path.dirname(__file__), 'poppler_windows', 'poppler-23.08.0', 'Library', 'bin')
            # old code for pre-installed poppler_path = os.path.join(os.path.dirname(__file__), 'poppler-0.68.0(win)', 'bin')

        elif platform.system() == "Linux":
            # Check if Poppler is already installed
            try:
                subprocess.run(["pdftoppm", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Poppler is already installed.")
                return
            except FileNotFoundError:
                pass

            # Install Poppler on Linux using the appropriate package manager
            package_managers = ["apt-get", "yum", "dnf"]
            for manager in package_managers:
                try:
                    subprocess.run(["sudo", manager, "install", "-y", "poppler-utils"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                    print("Poppler installed successfully.")
                    return
                except FileNotFoundError:
                    continue

            print("Poppler installation failed. Please install Poppler manually.")
            # old code for pre-installed poppler_path = os.path.join(os.path.dirname(__file__), 'poppler-23.06.0(linux)')

        elif platform.system() == "Darwin":  # macOS
            # Check if Poppler is already installed
            try:
                subprocess.run(["pdftoppm", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Poppler is already installed.")
                return

            except FileNotFoundError:
                pass

            # Install Poppler on macOS using Homebrew
            try:
                subprocess.run(["brew", "install", "poppler"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Poppler installed successfully.")

            except FileNotFoundError:
                print("Poppler installation failed. Please install Poppler manually.")
            return
        return poppler_path

    @staticmethod
    def save_img_to_temp(dataobj, logger, image, i, path_to_images):
        image_name = Path(ntpath.basename(dataobj.input_file)).stem
        image_path_string = f"{image_name}_page_{i + 1}.jpg"
        #image_path = dataobj.temp_dir + '\\' + os.path.normpath(image_path_string)
        image_path = os.path.join(dataobj.temp_dir, os.path.normpath(image_path_string)) # to also work in other os systems
        logger.info('Saving image to: ' + image_path, extra={'className': __class__.__name__})
        # TODO: do this with the rest of the library aswell
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
