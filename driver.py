from config import *
import re
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


def regexify():
    """Turn all criteria in database files as regular expressions."""
    regex_file_list = [file for file in os.listdir(DATABASE_DIR) if file.startswith("REGEX_") and file.endswith(".txt")]
    for file in regex_file_list:
        os.remove(os.path.join(DATABASE_DIR, file))


    file_list = [file for file in os.listdir(DATABASE_DIR) if file.endswith(".txt") and file != "blacklist.txt"]
    for file in file_list:
        with open(os.path.join(DATABASE_DIR, file), encoding="utf-16") as f1:
            with open(os.path.join(DATABASE_DIR, "REGEX_" + file), encoding="utf-16", mode="a+") as f2:
                line = f1.readline()
                while line:
                    criteria, cell_code = line.split("\t")
                    f2.write("^" + criteria + "$" + "\t" + cell_code)
                    line = f1.readline()

    with open(os.path.join(DATABASE_DIR, "blacklist.txt"), encoding="utf-16") as f3:
        with open(os.path.join(DATABASE_DIR, "REGEX_blacklist.txt"), encoding="utf-16", mode="a+") as f4:
            line = f3.readline()
            while line:
                f4.write("^" + line + "$")
                line = f3.readline()

def in_blacklist(string, blacklist):
    for pattern in blacklist:
        if re.search(pattern, string):
            return True
    return False


def lookup_database(string, database):
    for pattern, cell_code in database:
        print("pattern:", pattern, "|", "cell_code", cell_code)
        if re.search(pattern, string):
            return cell_code
    return ""


def init_database():
    """Initialize database by loading data from files in DATABASE_DIR"""
    # Construct BLACKLIST
    if "blacklist.txt" in os.listdir(DATABASE_DIR):
        with open(os.path.join(DATABASE_DIR, "blacklist.txt"), encoding="utf-16") as file_ptr:
            line = file_ptr.readline().strip()
            while line:
                BLACKLIST.add(line)
                line = file_ptr.readline().strip()

    # Construct database
    database_file_list = [file for file in os.listdir(DATABASE_DIR) if file.startswith("REGEX_") and file.endswith(".txt") and file != "REGEX_blacklist.txt"]

    for file in database_file_list:
        #print(file)
        with open(os.path.join(DATABASE_DIR, file), encoding="utf-16") as file_ptr:
            line = file_ptr.readline()
            while line:
                #print("line:", line)
                criteria, cell_code = line.strip().split("\t")
                line = file_ptr.readline()
                if in_blacklist(criteria, BLACKLIST):
                    continue
                elif not lookup_database(criteria, DATABASE):
                    DATABASE.append((criteria, cell_code))
                else:
                    # Check criteria/cell_code pair is correct
                    '''try:
                        if lookup_database(criteria, DATABASE) != cell_code:
                            error_msg = "Conflicting cell code for " + criteria
                            raise ValueError(error_msg)
                    except ValueError as error:
                        raise'''
                    if lookup_database(criteria, DATABASE) != cell_code:
                            error_msg = "Conflicting cell code for " + criteria + " in " + file + "\n" +\
                            "            Tried to encode " + criteria + " as " + cell_code + "\n" +\
                            "            But " + criteria + " is already registered as " + lookup_database(criteria, DATABASE)
                            raise ValueError(error_msg)


def map_cell_codes():
    """Map cell codes for all lines in files in INPUT_DIR."""
    file_list = [file for file in os.listdir(INPUT_DIR) if file.endswith(".txt")]

    for file in file_list:

        with open(os.path.join(INPUT_DIR, file), encoding="utf-16") as input_file_ptr:
            with open(os.path.join(OUTPUT_DIR, "MAPPED_" + file), encoding="utf-16", mode="a+") as output_file_ptr:
                line = input_file_ptr.readline()
                while line:
                    criteria, amount = line.strip().split("\t")
                    cell_code = lookup_database(criteria, DATABASE)
                    if cell_code:
                        output_file_ptr.write(criteria + "\t" + amount + "\t" + cell_code + "\n")
                    else:
                        output_file_ptr.write(criteria + "\t" + amount + "\n")
                    line = input_file_ptr.readline()


def main():
    """Driver's main program."""
    # Set up environment
    setup_env()

    # Clean output directory
    reset_directory(OUTPUT_DIR)

    # Preprocess database files
    regexify()

    # Load database
    init_database()

    # Process input files
    map_cell_codes()

    print("DATABASE:", DATABASE)
    print("BLACKLIST:", BLACKLIST)

if __name__ == "__main__":
    main()