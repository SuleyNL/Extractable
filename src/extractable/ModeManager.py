from enum import Enum
from PIL import Image
from matplotlib import pyplot as plt


class Mode(Enum):
    PERFORMANCE = 'performance'                 # maximize performance for big data ETL
    PRESENTATION = 'presentation'               # show every visual step in process
    PRESENTATION_PLUS = 'presentation plus'     # show every visual step in process, including irrelevant steps such as transforming images
    DEBUG = 'debug'                             # don't show every visual step, but do log all debugging-relevant information


def PDFtoImageConvertor_display_image(mode, image_path, i, len_images):
    if mode == Mode.PRESENTATION_PLUS:
        image_file = Image.open(image_path).convert("RGB")
        plt.imshow(image_file)
        plt.title('pdf is transformed to image(s) | number: ' + str(i + 1) + '/' + str(len_images))
        plt.axis('on')  # Optional: Turn off axis labels
        plt.show()


def TableDetector_display_image(mode, image, model, results, i, len_images):
    if mode == Mode.PRESENTATION:
        plot_results(image, model, results['scores'], results['labels'], results['boxes'],
                     title='Page number: ' + str(i + 1) + '/' + str(len_images) + ' | Tables detected: ' + str(
                         len(results["scores"])))


def TableDetector_display_table(mode, table_image, results, j):
    if mode == Mode.PRESENTATION:
        plt.imshow(table_image)
        plt.axis('on')
        plt.title(
            'cropped image of only table | number ' + str(j + 1) + ' out of ' + str(
                len(results["scores"])))
        plt.show()


def StructureDetector_display_structure(mode, image, model, presentation_results, i, len_images):
    if mode == Mode.PRESENTATION:
        plot_results(image, model, presentation_results['scores'], presentation_results['labels'],
                     presentation_results['boxes'],
                     'Recognized structure | table number ' + str(i + 1) + ' out of ' + str(len_images))


def TextExtractor_display_table(mode, image):
    if mode == Mode.DEBUG:  # TODO: SHOULD BE PRESENTATION once its confirmed to work
        # plt.figure(figsize=(2, 1))
        plt.imshow(image)
        plt.axis('on')
        plt.title(' image of all cells')
        plt.show()


def TextExtractor_display_cell(mode, cell_image, row, table_xml, read_roi12):
    if mode == Mode.DEBUG:  # TODO: SHOULD BE PRESENTATION once its confirmed to work
        plt.imshow(cell_image)
        plt.axis('on')
        plt.title('cropped image of only cell | number ' +
                  str(j + 1) + ' out of ' + str(len(row.cells) * len(table_xml.rows)) +
                  'text: ' + read_roi12['text'][-1])
        plt.show()


def plot_results(pil_img, model, scores, labels, boxes, title: str):
    plt.figure(figsize=(8, 5))
    plt.imshow(pil_img)
    ax = plt.gca()
    COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
              [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]
    colors = COLORS * 100
    drawn_boxes = []
    for score, label, (xmin, ymin, xmax, ymax), color in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
        alpha = 0.15
        linewidth = 1
        if model.config.id2label[label] == 'table row':
            text_x = 0 - (pil_img.height * 0.18)
            text_y = ((ymin + ymax) / 2)
            color = [0.850, 0.325, 0.098]

        elif model.config.id2label[label] == 'table column':
            text_x = ((xmin + xmax) / 2) - 80
            text_y = ymin - 15
            color = [0.350, 0.925, 0.098]

        elif model.config.id2label[label] == 'table':
            text_x = xmin + 30
            text_y = ymin - 50
            color = [0.000, 0.447, 0.741]

        else:
            text_x = ((xmin + xmax) / 2) - 100
            text_y = ((ymin + ymax) / 2) + 3
            color = [0.033, 0.045, 0.033]
            alpha = 0.05
            linewidth = 0
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, facecolor=color, alpha=0.3, linewidth=0))

        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=color, linewidth=linewidth))

        '''
        # Below code not that necessary yet, maybe in future with different type of pdf-tables. 
        # But for now adds unnecessary complexity

        # check if textbox overlaps with another textbox
        for drawn_box in drawn_boxes:
            while intersects(drawn_box, (xmin, ymin)):
                #if model.config.id2label[label] == 'table':
                xmin = max(xmin-10, 0)
                if xmin == 0:
                    ymin = max(ymin-10, 0)

                if xmin == 0 and ymin == 0:
                    break
        '''

        text = f'{model.config.id2label[label]}: {score:0.2f}'
        ax.text(text_x, text_y, text, fontsize=6,
                bbox=dict(facecolor=color, alpha=alpha))
        drawn_boxes.append([xmin, ymin])

    plt.axis('on')
    plt.title(title)
    plt.show()



