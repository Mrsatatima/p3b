from Tracker.tracker import *
from geo_script import *
from Matching.matching import  write_rrcollect_csv
from helper import kwara_lga_map, kwara_wards_map, wards_shapefile

to_capture_file_name = ""  # path to xlsx file of list of settlement to be captured
captured_file_name = ""   # rr_collect data of point captured
# lga map dict for names of lga in p3b vs names of lga on GRID3
# can be found on the helper module
# if not there you need to create yours
lga_dct = ""

# ward map dict for names of ward in p3b vs names of ward on GRID3
# can be found on the helper module
# if not there you need to create yours
ward_dct = ""


def main(state, to_capture_file_name, captured_file_name, ward_layer_file,lga_dict,ward_dct):
    """
        this runs all the processing that is need for tracking and validation
        it takes the file for the points to be capture and points already captured
        It first validates all the points captured for accuracy (they fall in the right boundary)
        then compare them with the points to be captured to see the progress and how may remain
        it creates file 1. point with accuracy issue 2. points yet to be capture
        Input:
            state: Name of state of interest (str)
            to_capture_file_name: path to the file contianing point to capture (str)
            captured_file_name: path to the file containing points captured
                                during data collection (str)
        Ouput:
            None

    """
    to_capture_df = pd.read_excel(to_capture_file_name)
    captured_df = pd.read_excel(captured_file_name)
    settlement_file_name, dh_file_name = write_rrcollect_csv(captured_df,True)

    settlement_layer = convert_csv_to_layer(settlement_file_name)
    wards_layer = QgsVectorLayer(ward_layer_file, "wards", "ogr")
    query = f'"statename"  =  \'{state}\''
    subset_wards_layer = crt_subset_lyr(wards_layer,query)
    new_settlement_layer = within_ward_boundary(settlement_layer,subset_wards_layer,lga_dict,ward_dct)

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
    main("Kwara",to_capture_file_name,captured_file_name,wards_shapefile,lga_dct, ward_dct)



