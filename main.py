from script import *
from geo_script import *

file_name = "2023_Kwara_P3B.xlsx"


def main():
    """
        this function 
    """
    sheets = get_sheets(file_name)
    # print(sheets,len(sheets))
    for sheet in sheets:
        # print(sheet)
        demo_df = pd.read_excel(file_name, sheet_name=sheet)
        row_index = actual_header_row(demo_df)
        clean_data = remove_first_blank_column(file_name, row_index, sheet)
        new_data = remove_unwanted_columns(clean_data, ["Wards", "List of contiguous communities/ settlements", "Population\n(2023)"])
        base_data = remove_blank_wards_rows(new_data)
        wards_df = drop_subtotal_rows(base_data)
        final_df = create_random_cluster(wards_df)
        write_to_excel(final_df, "Kwara_cluster.xlsx", sheet)
   