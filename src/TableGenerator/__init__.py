'''
Test Table Generator (TTG):
1. TableDataMaker = Generate synthetic Tabular data -> Faker
2. CreatePDFTable = Generate PDF table -> FPDF2
'''
from itertools import product
from src.TableGenerator.GenerateTableData import GenerateTableData
from src.TableGenerator.Options import OptionsENUM, Options
from src.TableGenerator.CreatePDFTable import GeneratePDFTable

options = Options()
params = options.__to_dict__()


def startProcess(output_dir: str, params: dict = params):
    # Import product function from the more_itertools module
    # Define the parameters for the GeneratePDFTable function as a dictionary

    # Use product() to create all possible combinations of parameter values
    for i, values in enumerate(product(*params.values())):

        # Combine each parameter-name and its' value of this iteration into a dict
        args = dict(zip(params.keys(), values))

        output_file = output_dir + str(i) + '.pdf'

        GenerateOneTable(output_file, args)


def GenerateOneTable(output_file, args):
    print()
    table_data = GenerateTableData(args[OptionsENUM.COLUMN_AMOUNT.value],
                                   args[OptionsENUM.ROW_AMOUNT.value],
                                   args[OptionsENUM.ROWS_IN_CELL.value])

    GeneratePDFTable(table_data, output_file, args)
    print("table generated at: " + output_file + ", with the following settings: " + str(args))



