from config import *
import shutil
import pandas as pd

def setup_env():
    """TODO: Download and upgrade modules if necessary."""
    pass


def reset_directory(dir_name):
    """Delete all files inside specified directory."""
    file_list = [os.path.join(dir_name, file) for file in os.listdir(dir_name)]
    for file in file_list:
        os.remove(file)


def init_database():
    """Initialize database by loading data from files in DATABASE_DIR"""
    # Construct BLACKLIST
    if "blacklist.txt" in os.listdir(DATABASE_DIR):
        with open(os.path.join(DATABASE_DIR, "blacklist.txt")) as file_ptr:
            line = file_ptr.readline().strip()
            while line:
                BLACKLIST.add(line)
                line = file_ptr.readline().strip()

    # Construct database
    database_file_list = [file for file in os.listdir(DATABASE_DIR) if file.endswith(".txt") and file != "blacklist.txt"]

    for file in database_file_list:
        #print(file)
        with open(os.path.join(DATABASE_DIR, file), encoding="utf-16") as file_ptr:
            line = file_ptr.readline()
            while line:
                criteria, cell_code = line.strip().split("\t")
                line = file_ptr.readline()
                if criteria in BLACKLIST:
                    continue
                elif criteria not in DATABASE:
                    DATABASE[criteria] = cell_code
                else:
                    # Check criteria/cell_code pair is correct
                    try:
                        if DATABASE[criteria] != cell_code:
                            error_msg = "Conflicting cell code for " + criteria
                            raise ValueError(error_msg)
                    except ValueError as error:
                        raise


def map_cell_codes():
    """Map cell codes for all lines in files in INPUT_DIR."""
    file_list = [file for file in os.listdir(INPUT_DIR) if file.endswith(".txt")]

    for file in file_list:

        with open(os.path.join(INPUT_DIR, file), encoding="utf-16") as input_file_ptr:
            with open(os.path.join(OUTPUT_DIR, "MAPPED_" + file), encoding="utf-16", mode="a+") as output_file_ptr:
                line = input_file_ptr.readline()
                while line:
                    criteria, cell_code = line.strip().split("\t")
                    if criteria in DATABASE:
                        output_file_ptr.write(criteria + "\t" + cell_code + "\t" + DATABASE[criteria] + "\n")
                    else:
                        output_file_ptr.write(criteria + "\t" + cell_code + "\n")
                    line = input_file_ptr.readline()


def main():
    """Driver's main program."""
    # Set up environment
    setup_env()

    # Clean output directory
    reset_directory(OUTPUT_DIR)

    # Load database
    init_database()

    # Process input files
    map_cell_codes()

    print(DATABASE)

if __name__ == "__main__":
    main()