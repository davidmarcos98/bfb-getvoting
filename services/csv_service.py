import csv
import json
from collections import defaultdict

from slugify import slugify


def generate_outcode_file(outcode: str, data: dict):
    with open(f'files/{outcode}.json', 'w') as f:
        json.dump(data, f)

def generate_files():
    data = defaultdict(lambda: defaultdict(str))
    with open("postcodes.csv", "r") as f:
        reader = csv.DictReader(f, delimiter=',')
        last_outcode = ''
        for row in reader:
            pc = row['Postcode'].strip()
            outcode, incode = tuple(pc.split(' '))
            if outcode != last_outcode: print(outcode)
            last_outcode = outcode
            constituency_slug = slugify(row['Constituency'])
            data[outcode][incode] = constituency_slug
    for outcode, incode_data in data.items():
        generate_outcode_file(outcode, incode_data)

generate_files()
