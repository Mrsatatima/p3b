import pandas as pd

from p3b import get_sheets, actual_header_row, remove_blank_wards_rows, remove_first_blank_column, remove_unwanted_columns, write_to_excel,get_lga_name
from Cluster.cluster import *
from helper import kwara_lga_map, kwara_wards_map

file_name = " "  # path to the p3b template
#  list of columns you only need
# e.g. ["Wards", "List of contiguous communities/ settlements", "Population\n(2023)"]
needed_columns = " "

# lga map dict for names of lga in p3b vs names of lga on GRID3
# can be found on the helper module
# if not there you need to create yours
lga_dct = ""

# ward map dict for names of ward in p3b vs names of ward on GRID3
# can be found on the helper module
# if not there you need to create yours
ward_dct = ""

state = ""  # state yo want to attach coordinats to  its p3b settlements



def main(state):
    """
        this function runs the whole process, it calls functions
        from script.py and geo_script.py it cleans the p3b create the cluster
        add google map direction link to each cluster. it then writes to an 
        excel file
        Input:
            state: Name of state you want to clean
        Output:
            none
    """
    sheets = get_sheets(file_name)
    # print(sheets,len(sheets))
    for sheet in sheets:
        # print(sheet)
        demo_df = pd.read_excel(file_name, sheet_name=sheet)
        row_index = actual_header_row(demo_df)
        clean_data = remove_first_blank_column(file_name, row_index, sheet)
        new_data = remove_unwanted_columns(clean_data, needed_columns)
        base_data = remove_blank_wards_rows(new_data)
        ward_list = []
        lga = get_lga_name(sheet)
        print(lga)
        if lga in kwara_security_challenged:
            ward_list = kwara_security_challenged[lga]
        wards_df = drop_subtotal_rows(base_data, ward_list)
        final_df = create_random_cluster(wards_df, state, lga, lga_dct, ward_dct)
        write_to_excel(final_df, f"{state}_cluster.xlsx", sheet)


if __name__ == "__main__":
    main("Kwara")