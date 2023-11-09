# Configure directories
from pathlib import Path
root = Path(__file__).parent / 'test_files/files/'

tables_dir = str(root / 'tables')
test_table_images_dir = str(root / 'test_table_images')
test_xmls_structures_dir = str(root / 'test_xml_structures')
test_table_structures_dir = str(root / 'test_table_structures')
test_images_dir = str(root / 'test_images')
table_pdf_file = str(root / 'tables/WNT1.pdf')
table_png_file_standard = str(root / 'tables/WNT-verantwoording2.png')
table_png_file_complex = str(root / 'tables/WNT-Verantwoording_2kolommen_in1.png')
empty_folder = str(root / 'empty_folder')
default_pdf_dir = str(root / 'generated_files')
default_pdf_file = str(root / 'generated_files/default')
temp_dir = str(root / 'fake_temp_dir')

