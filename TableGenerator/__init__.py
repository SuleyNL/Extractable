'''
Test Table Generator (TTG):
1. TableDataMaker = Generate synthetic Tabular data -> Faker
2. CreatePDFTable = Generate PDF table -> FPDF2
'''
from fpdf import FPDF

TABLE_DATA = (
    ("First name", "Last name", "Age", "City"),
    ("Jules", "Smith", "34", "San Juan"),
    ("Mary", "Ramos", "45", "Orlando"),
    ("Sul;eymen", "kands", "19", "Los Angeles"),
    ("Lucas", "Cimon", "31", "Saint-Mahturin-sur-Loire"),
)
pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", size=16)
with pdf.table(TABLE_DATA) as table:
    pass
pdf.output('table.pdf')
