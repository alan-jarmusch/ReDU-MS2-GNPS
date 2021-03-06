
import sys
sys.path.insert(0, "..")

from models import *
from collections import defaultdict
import csv

def main():
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    Compound.create_table(True)
    CompoundFilenameConnection.create_table(True)
    FilenameAttributeConnection.create_table(True)

    input_identifications = sys.argv[1]

    all_files_in_db = Filename.select()
    all_files_in_db_set = set([filename.filepath for filename in all_files_in_db])

    with open(input_identifications) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        line_count = 0
        for row in reader:
            line_count += 1

            if line_count % 1000 == 0:
                print(line_count)

            try:
                original_path = row["Original_Path"].replace("MSV000078556/spectrum", "MSV000078556/ccms_peak")


                if not original_path in all_files_in_db_set:
                    #print(original_path, "Missing")
                    continue

                filename_db = Filename.get(filepath=original_path)

                compound_db, status = Compound.get_or_create(compoundname=row['compound_name'])
                join_db = CompoundFilenameConnection.get_or_create(filename=filename_db, compound=compound_db)
            except KeyboardInterrupt:
                raise
            except:
                continue




if __name__ == '__main__':
    main()
