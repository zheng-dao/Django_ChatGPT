import argparse
import codecs
import csv
import json
import sys

from pyscape import Pyscape
from pyscape.fields import FIELDS

def batch_urls(urls, n):
    """n = size of batches. 10 is recommended."""
    for i in range(0, len(urls), n):
        yield urls[i:i+n]

def write_csv(outfile, data):
    "generate csv output"

    output = []
    headers = []
    keys = ["uu",
            "us",
            "upl",
            "ueid",
            "peid",
            "uipl",
            "pid",
            "pmrp",
            "ptrp",
            "upa",
            "pda",
            "ut",
            ]
        
    for k in keys:
        try:
            headers.append(FIELDS[k]['human'])
        except:
            headers.append(k)

    output.append(headers)

    for record in data:
        line = []
        try:
            for k in keys:
                if k in record:
                    line.append(record[k])
                else:
                    line.append('')
            output.append(line)
        except:
            output.append(['Error parsing line.'])

    writer = csv.writer(outfile, delimiter = ',',
                        quotechar = '"',
                        dialect = 'excel',
                        quoting = csv.QUOTE_ALL)
    writer.writerows(output)
    
parser = argparse.ArgumentParser(description = 'Interface with the Mozscape API to provide link metrics')
parser.add_argument('src', help = 'specify a text file with URLs')
parser.add_argument('dest', help = 'specify an output file')

#python pyscape-cli.py [input.txt] [output.csv]
def main():
    args = parser.parse_args()

    with open('./keys.json', 'r') as k:
        keys = json.load(k)
        
    p = Pyscape(**keys)
    
    urls = []
    with open(args.src, 'r') as s:
        for line in s:
            urls.append(line.rstrip())
    
    data = []
    for batch in batch_urls(urls, 10):
        data.extend(p.batch_url_metrics(batch).json())
        print('%s URLs returned' % (len(data)))

    with codecs.open(args.dest, 'w', encoding='utf-8') as outfile:
        write_csv(outfile, data)

if __name__ == '__main__':
    sys.exit(main())
