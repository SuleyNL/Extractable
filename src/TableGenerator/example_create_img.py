from genalog.pipeline import AnalogDocumentGeneration
from PIL import Image as im
import matplotlib.pyplot as plt
from genalog.degrader import ImageState
import requests


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

plt.imshow(img_array, cmap='gray')
plt.show()

