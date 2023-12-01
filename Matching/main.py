from Matching.matching import *
from p3b import get_sheets, actual_header_row, remove_first_blank_column,get_lga_name, populate_dh, populate_wards, write_to_excel
from helper import kwara_lga_map, kwara_wards_map

p3b_file = "2023_Kwara_P3B.xlsx" 
rr_collect_file = "RR_Collect_Merged_Form_Data (21).xlsx"
grid3_file = "Nigeria_-_Settlement_Points.csv"
lga_dct = kwara_lga_map
ward_dct = kwara_wards_map

def main(state, p3b, matching_data, grid3=True):
    """
        Runs the matching process for each Local Government Area (LGA) in Adamawa state.

        Reads in data files for settlements captured in grid3 and RR Collection exercises,
        as well as the P3B data for each LGA. Matches settlements in the P3B data to settlements in the
        grid3 and RR Collection data, then writes the results to separate Excel files for each LGA.

        Returns nothing.
    """
    # Read in the data files for settlements captured in grid3 and RR Collection exercises
    if grid3:

        matching_file= pd.read_csv(matching_data)
        matching_df = write_grid3_csv(matching_file, state)
    else:
        matching_file= pd.read_excel(matching_data)
        matching_df= write_rrcollect_csv(matching_file)
    sheets = get_sheets(p3b)
    #files where the matching with rr_collect and grid3 are to be save
    per_lga_match = f"{state}_match_grid3.xlsx"
    all_match = f"all_{state}_match_grid3.xlsx"
    all_perfect = {}
    all_no_match ={}
    # Create a dictionary to hold the matching results for each LGA
  
    # Iterate over each LGA
    for sheet in sheets:
        # Read in the P3B data for the current LGA
        df = pd.read_excel(p3b,sheet)
        header = actual_header_row(df)
        df = remove_first_blank_column(p3b,header,sheet)
        ward_pop = populate_wards(df)
        dh_pop = populate_dh(ward_pop)
        local_gov = get_lga_name(sheet)

        # Get a list of settlements in the P3B data for the current LGA
        # and the total number of settlements in the P3B data for the current LGA
        p3b_list  = get_p3b_list(dh_pop,local_gov)
        # Get a list of settlements captured in grid3 for the current LGA,
        # and match settlements in the P3B data to settlements in the grid3 data
        if grid3:
            grid3_list = get_captured_list(matching_df,local_gov,lga_dct, grid3=True)
        else:
            grid3_list = get_captured_list(matching_df,local_gov, lga_dct)



        # rr_collect_list = get_captured_list(rr_collect_file,local_gov,True)

        perfect = {}
        updated_p3B_list, updated_grid3_list, perfect, same_matched = matching_same_name(p3b_list,grid3_list,perfect,local_gov,lga_dct,ward_dct)

        # Match settlements in the P3B data that were not matched in the first pass to
        # settlements in the grid3 data using a similarity threshold of 0.9
        perfect, not_matched, similar_matched_7, updated_grid3_list = similar_name(updated_p3B_list, updated_grid3_list,perfect,local_gov,.9,lga_dct,ward_dct)

        # Match settlements in the P3B data that were not matched in the second pass to
        # settlements in the grid3 data using a similarity threshold of 0.75
        perfect, not_matched, similar_matched_5, updated_grid3_list= similar_name(not_matched,updated_grid3_list,perfect,local_gov,.75,lga_dct,ward_dct,dictionary=True)

        # Write the matching results to an Excel file for the current LGA
        final_data=create_final_data_frame(perfect,{},local_gov,True)
        write_to_excel(final_data, per_lga_match, local_gov)
        for key in perfect.keys():
            all_perfect[key] = perfect[key]
        for key in not_matched.keys():
            all_no_match[key] = not_matched[key]

        # Print a message indicating that the matching process for the current LGA is complete
        print("Done...........................................")
        print("Finish GRID3...........................................||||||||||||||||||||||||||||||||||")

        print("Done...........................................")

    final_all_data=create_final_data_frame(all_perfect,all_no_match,local_gov,True)
    write_to_excel(final_all_data,all_match,state)
    print("Finish...........................................")


if __name__ == "__main__":
    main("Kwara",p3b_file,grid3_file)