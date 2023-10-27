from script import *

file_name = "2023_Kwara_P3B.xlsx"


def main(state):
    """
        this function 
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
        new_data = remove_unwanted_columns(clean_data, ["Wards", "List of contiguous communities/ settlements", "Population\n(2023)"])
        base_data = remove_blank_wards_rows(new_data)
        ward_list = []
        if lga in kwara_security_challenged:
            ward_list = kwara_security_challenged[lga]
        wards_df = drop_subtotal_rows(base_data, ward_list)
        final_df = create_random_cluster(wards_df, state, lga)
        write_to_excel(final_df, f"{state}_cluster.xlsx", sheet)


if __name__ == "__main__":
    main("Kwara")