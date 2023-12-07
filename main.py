from p3b import *

file_name = ""  # path of the p3b template
state = ''  # the state you want to cleand its p3b


def main(state):
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
    for sheet in sheets:
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
    main(state)