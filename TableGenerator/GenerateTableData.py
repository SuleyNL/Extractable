import faker
import numpy as np


def GenerateTableData(column_amounts: int, row_amounts: int, rowsoftext_in_cell:int=1):
    # column_amounts refers to the amount of vertical columns
    # row_amounts refers to the amount of horizontal rows

    # Initialize faker to generate dutch data
    fake = faker.Faker(['nl_NL'])

    # Create a 2D ndarray with dimensions of rows x columns
    table_data = np.empty((row_amounts, column_amounts), dtype=object)

    # Generate a list of random sentences to use as the first column of the table, amount should be equal to the amount of rows
    for row_id in range(row_amounts):
        table_data[row_id][0] = fake.sentence(nb_words=3)

    # Generate a list of fake names to use as the header of the table, amount should be equal to the amount of columns -1
    for column_id in range(1, column_amounts):
        table_data[0][column_id] = fake.name()

    # Generate a 2D array of fake price tags to use as the body of the table
    for column_id in range(1, column_amounts):
        for row_id in range(1, row_amounts):
            table_data[row_id][column_id] = fake.pricetag()

    return table_data
