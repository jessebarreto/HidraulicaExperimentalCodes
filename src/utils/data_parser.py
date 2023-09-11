import csv
import typing

def parse_data(filepath: str) -> typing.List[str]:
    rows = []
    with open(filepath, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=";", quotechar='|')
        for row in data:
            rows.append(row)
    return rows
        

def convert_csv_to_measurements_as_str(rows: typing.List[str]) -> typing.Dict[str, typing.List[str]]:
    header = rows[0]

    measurements_as_str = {}
    for header_entry in header:
        if header_entry not in measurements_as_str:
            trimmed_entry = header_entry.strip(' "')
            measurements_as_str[trimmed_entry] = []

    for row in rows[1:]:
        zipped_key_value = zip(measurements_as_str.keys(), row)
        for key, value in zipped_key_value:
            measurements_as_str[key].append(value)

    return measurements_as_str


def write_data(filepath:str, lines:typing.List[str]) -> bool:
    with open(filepath, 'w', newline='') as csvfile:
        for line in lines:
            csvfile.write(line)
            csvfile.write("\n")
    return True