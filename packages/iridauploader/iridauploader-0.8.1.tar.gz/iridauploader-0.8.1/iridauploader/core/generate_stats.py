from iridauploader import parsers
from iridauploader.parsers.common import find_directory_list, get_file_list

import os
import pdb
import csv
import pandas as pd
import pprint
pp = pprint.PrettyPrinter()

out_file = "/home/CSCScience.ca/jthiessen/git/irida-uploader/stats.csv"


# list_of_dirs_with_runs = [
#     "/home/CSCScience.ca/jthiessen/git/irida-uploader/examples",
#     "/home/CSCScience.ca/jthiessen/git/irida-uploader/iridauploader/tests_integration"
# ]

list_of_dirs_with_runs = [
    "/Drives/W/Sequencing/Instrument/MiSeq",
    "/Drives/W/Sequencing/Instrument/MiSeq/windows_10_uploads",
    "/Drives/W/Sequencing/Instrument/MiSeq-HIV",
    "/Drives/W/Sequencing/Instrument/MiniSeq",
    "/Drives/W/Sequencing/Instrument/NextSeq",
    "/Drives/W/Sequencing/Instrument/NextSeq-NLHG",
]

parser_list_config = ["miseq", "miseq_win10_jun2021", "nextseq", "miniseq"]

print("file loaded")


def main():
    print("starting...")
    directory_list = make_super_list(list_of_dirs_with_runs)
    my_data = get_data_from_dir(parser_list_config, directory_list)
    # pp.pprint(my_data)
    df = pd.DataFrame(my_data)
    df.to_csv(out_file, sep='\t', encoding='utf-8', index=False)


class DataLine:
    def __init__(self, directory_name, date, sample_count, parent_dir_name):
        s_type = DataLine._get_s_type(parent_dir_name)
        self._data = {"directory name": directory_name,
                      "date": date,
                      "sample count": sample_count,
                      "folder": parent_dir_name,
                      "sequencer": s_type
                      }

    @property
    def data(self):
        return self._data

    @staticmethod
    def _get_s_type(dir_name):
        if dir_name in ["MiSeq", "MiSeq-HIV", "windows_10_uploads"]:
            return "miseq"
        elif dir_name in ['MiniSeq']:
            return "miniseq"
        elif dir_name in ["NextSeq", "NextSeq-NLHG"]:
            return "nextseq"


def make_super_list(dir_list):
    big_list = []
    for l in dir_list:
        new_list = find_directory_list(l)
        big_list = big_list + new_list
    return big_list


def get_data_from_dir(parser_list, d_list):
    data_list = []

    for directory in d_list:
        data_line = None
        for parser_type in parser_list:
            data_line = None
            try:
                date_data = get_date_from_directory(directory)
                sample_count = get_sample_count_from_directory(parser_type, directory)
                dir_name = get_parent_dir_from_directory(directory)
                data_line = DataLine(directory, date_data, sample_count, dir_name)
                data_list.append(data_line.data)
                break
            except parsers.exceptions.DirectoryError:
                continue
            except Exception as e:
                print("exception encountered...")
                print(e)
                print()
                continue
        if data_line is None:
            print("NO DATA")
            data_line = DataLine(directory, None, 0, None)
            data_list.append(data_line.data)

    return data_list


def get_date_from_directory(directory):
    base_path = os.path.basename(os.path.normcase(directory))
    dir_id = base_path[0:6]
    dyear = "20" + dir_id[0:2]
    dmonth = dir_id[2:4]
    dday = dir_id[4:6]
    d = dyear + "-" + dmonth + "-" + dday
    return d


def get_parent_dir_from_directory(directory):
    return os.path.basename(os.path.dirname(directory))


def get_sample_count_from_directory(parser_type, directory):
    parser = parsers.parser_factory(parser_type)
    sample_sheet = parser.get_sample_sheet(directory)
    # s_run = parser.get_sequencing_run(sample_sheet)
    # count = 0
    # for p in s_run.project_list:
    #     count = count + len(p.sample_list)
    count = get_count_from_sheet(sample_sheet)
    return count


def get_count_from_sheet(sheet):
    in_data_section = False
    count = 0
    with open(sheet) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if in_data_section:
                if len(row) != 0:
                    count = count + 1
            elif row == ['[Data]']:
                in_data_section = True
                count = -1  # skip header count

    return count


# This is called when the program is run for the first time
if __name__ == "__main__":
    main()
