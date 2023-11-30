import pandas as pd
from Matching.matching import get_captured_list, get_p3b_list,  match_phrases
import openpyxl
import os

def create_dict(LGA,to_capture_dict,captured_dict):
    dict ={} 
    capture_list ={}
    for local_gov in LGA:
        capture_list = get_captured_list(captured_dict,local_gov,captured_list=capture_list)
        lga_total = 0
        dict[local_gov.lower()] = {}
        for indx in range(len(to_capture_dict)):
            if to_capture_dict["LGA"][indx].lower() == local_gov.lower():
                if to_capture_dict["Ward"][indx] not in dict[local_gov.lower()]:
                    dict[local_gov.lower()][to_capture_dict['Ward'][indx]] = []
                dict[local_gov.lower()][to_capture_dict['Ward'][indx]].append(to_capture_dict["Settlement"][indx])
    return dict, capture_list