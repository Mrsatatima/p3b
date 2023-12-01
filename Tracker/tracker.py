import pandas as pd
from Matching.matching import get_captured_list, get_p3b_list,  match_phrases
from p3b import write_to_excel
import openpyxl
import os


def create_to_capture_dict(LGA,to_capture_df,captured_df):
    """
        this function creates two dictionary from two files
        i.e. the points to be captured and points captured
        during a data collection
        Input:
            LGA: local government the data collection
                is taking place(atr)
            to_capture_df: All points to be captured (pandas dataframe)
            captured_df: All points that have been 
                    captured (pandas dataframe)
    """
    to_capture_dict ={} 
    capture_list ={}
    for local_gov in LGA:
        capture_list = get_captured_list(captured_df, local_gov, {}, captured_list=capture_list)
        to_capture_dict[local_gov.lower()] = {}
        for indx in range(len(to_capture_df)):
            if to_capture_df["LGA"][indx].lower() == local_gov.lower():
                if to_capture_df["Ward"][indx] not in to_capture_dict[local_gov.lower()]:
                    to_capture_dict[local_gov.lower()][to_capture_df['Ward'][indx]] = []
                to_capture_dict[local_gov.lower()][to_capture_df['Ward'][indx]].append(to_capture_df["Settlement"][indx])
    return to_capture_dict, capture_list


def match(to_capture_list,capture_list):
    """
        this funtions take teo dictionary of settlements to capture
        and settlments captured. It then compares the teo dict and writes 
        3 excel files of list of settlments captured per ward for each lga, 
        list of settlements yet to be captured per ward for each lga and 
        a summary of total settlements capture per lga aand per ward
        Input:
            to_capture_list: a dictionary fo all settlements that needs to be
                        captured (dict)
            capture_list: a dictionary of settlements capture so far (dict)
        Output:
            None
    """
    #per ward summary data
    sum_lga =[]
    sum_ward = []
    sum_settlement = []
    sum_cap_sett = []


    #per lga capture summary data
    total_lga =[]
    total_settlement =[]
    total_cap_settlement =[]

    for lga, wards in to_capture_list.items():
        # print(lga)
        sum = 0 # per lga settlements to capture
        total_lga.append(lga)
        
        lga_sum = 0 # per lga settlements captured
        for ward, settlements in wards.items():
            # settlements yet to be captured per ward data
            cap_lga =[]
            cap_ward = []
            not_cap_set = set()

            # settlements  captured per ward
            y_cap_lga =[]
            y_cap_ward = []
            y_not_cap_set = set()
            # lga_sum+=1
            
            # add data to per ward summary data
            sum_lga.append(lga)
            sum_ward.append(ward)
            sum_settlement.append(len(settlements))

            # increase per lga count
            sum+=len(settlements)

            sum_set = 0 # per ward settlements captured
            # print(settlements, len(settlements), ward)

            for settlement in settlements:
                wards_match = [] # keeps matched settlements

                # if any data for this lga has been captured
                if lga.lower().strip() in capture_list: 

                     # if any data for this ward has been captured
                    if ward.lower().strip() in capture_list[lga.lower().strip()]:

                        for cap_set in capture_list[lga.lower().strip()][ward.lower().strip()].keys():
                            if str(settlement).lower().strip() == str(cap_set).strip().lower():
                                sum_set+=1 # increase settlement capture per ward

                                wards_match.append(settlement)

                                # adds matched settlement to captured data
                                y_cap_lga.append(lga)
                                y_cap_ward.append(ward)
                                y_not_cap_set.add(settlement)
                                # break
                        # checks if a settlemnt was not successfully matched
                        if settlement not in wards_match:

                            # adds unmatched settlement to  yet to be captured data
                            not_cap_set.add(settlement)
                            cap_lga.append(lga)
                            cap_ward.append(ward)
                            # break
                    else:  #if entire ward not covered
                        # adds unmatched settlement to  yet to be captured data
                        not_cap_set.add(settlement)
                        cap_lga.append(lga)
                        cap_ward.append(ward)
                else:  #if entire lga not covered
                    # adds unmatched settlement to  yet to be captured data
                    not_cap_set.add(settlement)
                    cap_lga.append(lga)
                    cap_ward.append(ward)
            # print(sum_set)

            # add total captured to per ward summary data
            sum_cap_sett.append(sum_set)

            lga_sum+=sum_set #increase per lga settlements captured

            captured_ward_df = pd.DataFrame({"LGA":y_cap_lga[:len(y_not_cap_set)],"Ward":y_cap_ward[:len(y_not_cap_set)], "Settlement":list(y_not_cap_set)})
            not_captured_ward_df = pd.DataFrame({"LGA":cap_lga[:len(not_cap_set)],"Ward":cap_ward[:len(not_cap_set)], "Settlement":list(not_cap_set)})
            

            write_to_excel(captured_ward_df,f"lga\\captured\\{lga}.xlsx", f'{ward.replace("/"," ")}')
            write_to_excel(not_captured_ward_df,f"lga\\not_captured\\{lga}.xlsx", f'{ward.replace("/"," ")}')

        # append to lga summary data
        total_settlement.append(sum)
        total_cap_settlement.append(lga_sum)
        
    summary_df = pd.DataFrame({"LGA":sum_lga,"Ward":sum_ward,"Total settlement to capture":sum_settlement,
                                "Total Settlement Captured":sum_cap_sett}, index=None)
    summary_lga = pd.DataFrame({"LGA":total_lga,"Total settlement to capture":total_settlement,
                                "Total settlement captured":total_cap_settlement}, index=None)
    
    with pd.ExcelWriter('Geo Coordinate Capture Summary.xlsx') as writer:
        summary_lga.to_excel(writer, sheet_name='Total per LGA')
        summary_df.to_excel(writer, sheet_name='Total per Ward')


def write_within_boundary_xlx(data_frame):
    lgas = list(data_frame.LGA.unique)
    for lga in lgas:
        selection = data_frame['LGA'] == lga
        col =  ['State', 'LGA', 'Ward',"Name of ettlement","in_Ward","dst_km"]
        lga_df = data_frame.loc[selection,col]
        wards = list(lga_df.Ward.unique())
        for ward in wards:
            selection = lga_df['Ward'] == ward
            ward_df = lga_df[selection]
            write_to_excel(ward_df,f"lga\\out_boundary\\{lga}.xlsx", f'{ward.replace("/"," ")}')

