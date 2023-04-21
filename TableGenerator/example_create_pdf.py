import genalog
from genalog.pipeline import AnalogDocumentGeneration
import requests
import cv2
from PIL import Image as im
import numpy as np
import matplotlib.pyplot as plt
import requests
from genalog.generation.content import CompositeContent, ContentType
from genalog.generation.document import DocumentGenerator

sample_text_url = "https://raw.githubusercontent.com/microsoft/genalog/main/example/sample/generation/example.txt"

r = requests.get(sample_text_url, allow_redirects=True)
text = r.content.decode("ascii")

# Initialize CompositeContent Object
paragraphs = text.split('\n\n')  # split paragraphs by `\n\n`
content_types = [ContentType.PARAGRAPH] * len(paragraphs)
content = CompositeContent(paragraphs, content_types)

default_generator = DocumentGenerator()

# Select specific template, content and create the generator
doc_gen = default_generator.create_generator(content, ['letter.html.jinja'])
# we will use the `CompositeContent` object initialized from above cell
# python generator

for doc in doc_gen:
    doc.render_pdf(target="example_text_block1.pdf")

    # PDF to image so it can be displayed
    image_byte = doc.render_png(resolution=300)
    nparr = np.frombuffer(image_byte, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize the image to fit the screen
    scale_percent = 50  # adjust as needed
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # Display the resized image using imshow

    # Display the image using plt.imshow()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Image ({img.shape[1]}x{img.shape[0]})")
    plt.show()

'''

# You can add as many options as possible. A new document will be generated per combination of the styles
new_style_combinations = {
    "hyphenate": [True],
    "font_size": ["11px", "12px"], # most CSS units are supported `px`, `cm`, `em`, etc...
    "font_family": ["Times"],
    "text_align": ["justify"]
}

default_generator = DocumentGenerator()
default_generator.set_styles_to_generate(new_style_combinations)
# Example the list of all style combination to generate
print(f"Styles to generate: {default_generator.styles_to_generate}")

doc_gen = default_generator.create_generator(content, ["columns.html.jinja", "letter.html.jinja"])

for doc in doc_gen:
    image_byte = doc.render_png(resolution=300)
    nparr = np.frombuffer(image_byte, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize the image to fit the screen
    scale_percent = 50  # adjust as needed
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # Display the resized image using imshow

    # Display the image using plt.imshow()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Image ({img.shape[1]}x{img.shape[0]})")
    plt.show()

'''