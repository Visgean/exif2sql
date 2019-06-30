#!/usr/bin/env python3

from pathlib import Path
import argparse
import utils
from sqlalchemy import create_engine

parser = argparse.ArgumentParser(description="Generate sql database with exif data.")
parser.add_argument('picture_folders', nargs='+', help='Folders with the images')

parser.add_argument(
    '-s', '--sqlite',
    help='Output the data frame to SQLite file (this will override existing file!)',
)

parser.add_argument(
    '-f', '--feather',
    help='Output the data frame to feather file (this will override existing file!)',
)

parser.add_argument(
    '-e', '--excel',
    help='Output the data frame to excel (this will override existing file!)',
)


parser.add_argument(
    '-p', '--processes',
    type=int,
    help='number of processes to use for collecting exif data, defaults to 5',
    default=5
)


def main():
    args = parser.parse_args()
    df = utils.get_panda_df(
        [Path(f).resolve() for f in args.picture_folders],
        processes=args.processes
    )

    if args.sqlite:
        sql_file = Path(args.sqlite).resolve()
        if sql_file.exists():
            sql_file.unlink()
        engine = create_engine(f'sqlite:///{sql_file}', echo=False)
        df.to_sql('photos', con=engine)

    if args.feather:
        feather_file = Path(args.feather).resolve()
        if feather_file.exists():
            feather_file.unlink()
        df.to_feather(feather_file)

    if args.excel:
        excel_file = Path(args.excel).resolve()
        if excel_file.exists():
            excel_file.unlink()
        df.to_excel(excel_file)


if __name__ == '__main__':
    main()