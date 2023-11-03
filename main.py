from script import *

file_name = "2021_Ogun_P3B.xlsx"
needed_columns = ["Wards", "List of contiguous communities/ settlements", "Population\n(2021)"]
lga_dct = ogun_lga_map
ward_dct = ogun_wards_map


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
        lga = sheet.split('.')[1].strip().lower().title()
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


if __name__ == "__main__":
    main("Ogun")