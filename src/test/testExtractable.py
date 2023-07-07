from Extractable import Extractor
from Extractable.library import *

# Extractor.extract_using_TATR_OCR('src/test/files/WNT1.pdf', 'src/test/files/WNT1/wnt1', mode=Mode.DEBUG)
#  Extractor.extract_using_TATR('src/test/files/tables/default.pdf', 'src/test/files/tables/default.pdf', mode=Mode.PRESENTATION)


#TEST
# Prob wrong PPI
#Extractor.extract('src/test/files/error_pdfs/no_rows/1.pdf', 'src/test/files/error_pdfs/no_rows/1.pdf', mode=Mode.PRESENTATION)
# Low accuracy cols & rows
#Extractor.extract('src/test/files/error_pdfs/no_text/1.pdf', 'src/test/files/error_pdfs/no_text/1.pdf', mode=Mode.PRESENTATION)
# Detects rotated tables but cant parse them into columns and rows
#Extractor.extract('src/test/files/error_pdfs/no_text/2.pdf', 'src/test/files/error_pdfs/no_text/2.pdf', mode=Mode.PRESENTATION)

# Multiple overlapping tables, and horizontal pages
Extractor.extract('src/test/files/error_pdfs/some_error/Data Fact Sheet - 2022 Microsoft Sustainability Report.pdf',
                  'src/test/files/error_pdfs/some_error/Data Fact Sheet - 2022 Microsoft Sustainability Report.pdf',
                  mode=Mode.PRESENTATION)





