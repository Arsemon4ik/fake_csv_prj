# import os
# from django.conf import settings
from faker import Faker
import csv
import uuid
# from pprint import pprint

FAKE = Faker(locale='en_US')
# FOLDER_PATH = os.path.join(settings.BASE_DIR, 'media/')
dialect = csv.Dialect


def check_order_duplicates(order_list: list) -> bool:
    """ Check if given list contains any duplicates """

    if len(order_list) == len(set(order_list)):
        return False
    else:
        return True


def counts_none_in_tuple(fake_range: tuple) -> int:
    checked_list = list(filter(lambda x: x is not None, fake_range))
    return len(checked_list)


def get_dummy_data_by_type(field_type: str, fake_range: tuple) -> str:
    """ Takes field type and range, return random string based on the type """

    if field_type == 'full_name':
        return FAKE.name()
    elif field_type == 'job':
        return FAKE.job()
    elif field_type == 'email':
        return FAKE.email()
    elif field_type == 'phone_number':
        return FAKE.phone_number()
    elif field_type == 'company':
        return FAKE.company()
    elif field_type == 'date':
        return FAKE.date()
    elif field_type == 'domain_name':
        return FAKE.domain_name()
    elif field_type == 'address':
        return FAKE.address()
    elif field_type == 'integer':
        if counts_none_in_tuple(fake_range) == 2:
            return FAKE.random_int(*fake_range)  # *fake_range - (from, to)
        else:
            return FAKE.random_int(1, 100)  # if arguments are None - (1, 100) default
    elif field_type == 'text':
        if counts_none_in_tuple(fake_range) == 1:
            # variable_nb_sentences=False - generates the exact amount
            return FAKE.paragraph(fake_range[1], variable_nb_sentences=False)
        else:
            return FAKE.paragraph(5)  # if all arguments are None - (5 sentences) default


def create_dummy_data(fieldnames: list, field_types: list, rows: int, fake_rage: list[tuple]) -> list:
    """ Takes field names, field types, number of rows, range and returns a list of fake data """
    data = []

    for _ in range(rows):
        row = {}
        for index, value in enumerate(fieldnames):
            row[value] = get_dummy_data_by_type(field_types[index], fake_rage[index])
        data.append(row)
    return data


def create_fake_csv(filename: str,
                    fieldnames: list[str],
                    order: list[int],
                    field_range: list[tuple],
                    delimiter: str,
                    string_character: str,
                    field_types: list[str],
                    rows: int) -> str:
    """
    Takes file name, field names, order, field types, number of rows, range, delimiter, string_character
    creates a csv file and returns a path of this file
    """

    ordered_field_names = [fieldnames[inx-1] for inx in order]
    ordered_field_types = [field_types[inx-1] for inx in order]

    dummy_data = create_dummy_data(fieldnames=ordered_field_names, field_types=ordered_field_types, rows=rows, fake_rage=field_range)
    _uuid = uuid.uuid4()
    new_file_path = f'/home/arsemon4ik/fake_csv_prj/media/{filename}{_uuid}.csv'

    dialect.delimiter = delimiter
    dialect.quoting = csv.QUOTE_MINIMAL
    dialect.quotechar = string_character if string_character else '"'
    dialect.lineterminator = '\n'

    with open(new_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ordered_field_names, dialect=dialect)
        writer.writeheader()
        writer.writerows(dummy_data)

    return f'{filename}{_uuid}.csv'
