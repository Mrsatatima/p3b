import pandas as pd

from p3b import get_sheets, actual_header_row, remove_blank_wards_rows, remove_first_blank_column, remove_unwanted_columns, write_to_excel
from cluster import *
from helper import kwara_lga_map, kwara_wards_map

file_name = "2023_Kwara_P3B.xlsx"
needed_columns = ["Wards", "List of contiguous communities/ settlements", "Population\n(2021)"]
lga_dct = kwara_lga_map
ward_dct = kwara_wards_map


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
    for sheet in sheets[9:]:
        # print(sheet)
        lga_list = sheet.split('.')
        try:
            lga = lga_list[1].strip().lower().title()
        except:
            lga = lga_list.strip().lower().title()
        print(lga)
        demo_df = pd.read_excel(file_name, sheet_name=sheet)
        row_index = actual_header_row(demo_df)
        clean_data = remove_first_blank_column(file_name, row_index, sheet)
        new_data = remove_unwanted_columns(clean_data, needed_columns)
        base_data = remove_blank_wards_rows(new_data)
        ward_list = []
        if lga in kwara_security_challenged:
            ward_list = kwara_security_challenged[lga]
        wards_df = drop_subtotal_rows(base_data, ward_list)
        final_df = create_random_cluster(wards_df, state, lga, lga_dct, ward_dct)
        write_to_excel(final_df, f"{state}_cluster.xlsx", sheet)


def populate_p3b_main(state):
    """
        this function runs the whole process for populating the p3b,
        it calls functions from script.py,it cleans the p3b by setting
        the actual header and populating wards and DHs. it then writes
        to an excel file
        Input:
            state: Name of state you want to clean
        Output:
            none
    """

    sheets = get_sheets(file_name)
    for sheet in sheets[14:]:
        lga_list = sheet.split('.')
        try:
            lga = lga_list[1].strip().lower().title()
        except:
            lga = lga_list[0].strip().lower().title()
        print(lga)
        demo_df = pd.read_excel(file_name, sheet_name=sheet)
        row_index = actual_header_row(demo_df)
        clean_data = remove_first_blank_column(file_name, row_index, sheet)
        ward_pop_df = populate_wards(clean_data)
        dh_pop_df = populate_dh(ward_pop_df)
        write_to_excel(dh_pop_df, f"{state}_p3b_populated.xlsx", sheet)


if __name__ == "__main__":
    main("Kwara")