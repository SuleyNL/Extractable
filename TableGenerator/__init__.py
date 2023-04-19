import genalog
from genalog.pipeline import AnalogDocumentGeneration
import requests
import cv2
from IPython.core.display import Image, display
from PIL import Image as im
import numpy as np
import matplotlib.pyplot as plt
from genalog.degradation.degrader import ImageState
import requests
from genalog.generation.content import CompositeContent, ContentType
from genalog.generation.document import DocumentGenerator
from IPython.core.display import Image, display
from genalog.generation.document import DocumentGenerator
from IPython.core.display import Image, display


#CONFIGURATIONS
STYLE_COMBINATIONS = {
    "language": ["en_US"],
     "font_family": ["Segeo UI"],
     "font_size": ["12px"],
     "text_align": ["justify"],
     "hyphenate": [True],
}
HTML_TEMPLATE = "columns.html.jinja"

#DEGRADATIONS

DEGRADATIONS = [
    ("blur", {"radius": 5}),
    ("bleed_through", {
        "src": ImageState.CURRENT_STATE,
        "background": ImageState.ORIGINAL_STATE,
        "alpha": 0.8,
        "offset_x": -6,
        "offset_y": -12,
    }),
    ("morphology", {"operation": "open", "kernel_shape":(9,9), "kernel_type":"plus"}),
    ("pepper", {"amount": 0.005}),
    ("salt", {"amount": 0.15}),
]

#CREATE A DOCUMENT IMG

sample_text_url = "https://raw.githubusercontent.com/microsoft/genalog/main/example/sample/generation/example.txt"
sample_text = "example.txt"

r = requests.get(sample_text_url, allow_redirects=True)
open(sample_text, 'wb').write(r.content)

IMG_RESOLUTION = 300 # dots per inch (dpi) of the generated pdf/image

doc_generation = AnalogDocumentGeneration(styles=STYLE_COMBINATIONS, degradations=DEGRADATIONS, resolution=IMG_RESOLUTION, template_path=None)

# for custom templates, please set template_path.
img_array = doc_generation.generate_img(sample_text, HTML_TEMPLATE, target_folder=None) # returns the raw image bytes if target_folder is not specified

# creating image object of
# above array
data = im.fromarray(img_array)

# saving the final output
# as a PNG file
data.save('gfg_dummy_pic.png')

_, encoded_image = cv2.imencode('.png', img_array)
display(Image(data=encoded_image, width=600))

#CREATE A DOCUMENT PDF

sample_text_url = "https://raw.githubusercontent.com/microsoft/genalog/main/example/sample/generation/example.txt"

r = requests.get(sample_text_url, allow_redirects=True)
text = r.content.decode("ascii")


# Initialize CompositeContent Object
paragraphs = text.split('\n\n') # split paragraphs by `\n\n`
content_types = [ContentType.PARAGRAPH] * len(paragraphs)
content = CompositeContent(paragraphs, content_types)

default_generator = DocumentGenerator()

#print(f"Available default templates: {default_generator.template_list}")
#print(f"Default styles to generate: {default_generator.styles_to_generate}")


doc_gen = default_generator.create_generator(content, ['text_block.html.jinja'])

for doc in doc_gen:
    image_byte = doc.render_png(resolution=100)
    display(Image(image_byte))

# Select specific template, content and create the generator
doc_gen = default_generator.create_generator(content, ['text_block.html.jinja'])
# we will use the `CompositeContent` object initialized from above cell

# python generator
for doc in doc_gen:
    doc.render_pdf(target="example_text_block1.png")



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
# Create a new Genalog table
my_table = core.Table(name="Sample Table")

# Add columns to the table
my_table.add_column("ID", core.DataType.INTEGER)
my_table.add_column("Name", core.DataType.STRING)
my_table.add_column("Age", core.DataType.INTEGER)

# Add rows to the table
my_table.add_row([1, "Alice", 25])
my_table.add_row([2, "Bob", 32])
my_table.add_row([3, "Charlie", 41])

# Create a new Genalog document
my_doc = core.Document(name="Sample Document")

# Add the table to the document
my_doc.add_table(my_table)

# Save the document as a PDF file
my_doc.save_as_pdf("sample_table.pdf")
'''
