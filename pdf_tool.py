import argparse
import glob
import os
import os.path as path
from enum import Enum

from PyPDF2 import PdfReader, PdfWriter


class Mode(Enum):
    MERGE = 'merge'
    SPLIT = 'split'


def merge(file_paths):

    writer = PdfWriter()
    for source in file_paths:

        print(f'Processing {os.path.splitext(os.path.basename(source))[0]}...')
        reader = PdfReader(source)

        for page in range(0, len(reader.pages)):
            writer.add_page(reader.pages[page])

    with open(os.path.join(os.path.dirname(file_paths[0]), 'merged.pdf'), 'wb') as out:
        writer.write(out)


def split(file_path, page_from=None, page_to=None):

    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in range((page_from - 1) if page_from else 0,
                      page_to if page_to is not None else len(reader.pages)):
        writer.add_page(reader.pages[page])

    with open(f'{path.basename(file_path).split(path.extsep)[0]}_split.pdf', 'wb') as out:
        writer.write(out)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['merge', 'split'], required=True)
    parser.add_argument('--page-from', type=int, help=f'Page to start from (inclusive) when running in `{Mode.SPLIT.value}` mode')
    parser.add_argument('--page-to', type=int, help=f'Page to finish at (inclusive) when running in `{Mode.SPLIT.value}` mode')
    parser.add_argument('globs', type=str, nargs='+')

    args = parser.parse_args()

    file_paths = [y for x in args.globs for y in glob.glob(x)]

    resulting_paths = []
    for x in file_paths:
        if x not in resulting_paths:
            resulting_paths.append(x)

    print(resulting_paths)
    

    match args.mode:
        case Mode.MERGE.value:
            merge(resulting_paths)
        case Mode.SPLIT.value:
            for x in resulting_paths:
                split(x, args.page_from, args.page_to)
