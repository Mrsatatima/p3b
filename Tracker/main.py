from Tracker.tracker import *
from geo_script import *
from Matching.matching import  write_rrcollect_csv
from helper import kwara_lga_map, kwara_wards_map, wards_shapefile

to_capture_file_name = "merged_list.xlsx"
captured_file_name = "RR_Collect_Merged_Form_Data (21).xlsx"


def main(state,to_capture_file_name, captured_file_name,ward_layer_file,lga_map,ward_map):
    """
    """
    to_capture_df = pd.read_excel(to_capture_file_name)
    captured_df = pd.read_excel(captured_file_name)
    settlement_file_name, dh_file_name = write_rrcollect_csv(captured_df,True)

    settlement_layer = convert_csv_to_layer(settlement_file_name)
    wards_layer = QgsVectorLayer(ward_layer_file, "wards", "ogr")
    query = f'"statename"  =  \'{state}\''
    subset_wards_layer = crt_subset_lyr(wards_layer,query)
    new_settlement_layer = within_ward_boundary(settlement_layer,subset_wards_layer,lga_map,ward_map)

    query = '"in_Ward" = \'No\''
    no_new_layer = crt_subset_lyr(new_settlement_layer,query)
    no_layer_data_frame = convert_layer_to_dataframe(no_new_layer)
    write_within_boundary_xlx(no_layer_data_frame)

    query = '"in_Ward" = \'Yes\''
    yes_new_layer = crt_subset_lyr(new_settlement_layer,query)
    yes_layer_data_frame = convert_layer_to_dataframe(yes_new_layer)
    lgas = list(yes_layer_data_frame.LGA.unique())
    to_capture_list, captured_list = create_to_capture_dict(lgas,to_capture_df,yes_layer_data_frame)
    match(state, to_capture_list,captured_list)



if __name__ == "__main__":
    main("Kwara",to_capture_file_name,captured_file_name,wards_shapefile,kwara_lga_map,kwara_wards_map)



