import pandas as pd
from Matching.matching import get_captured_list, get_p3b_list,  match_phrases
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
        capture_list = get_captured_list(captured_df,local_gov,{},captured_list=capture_list)
        to_capture_dict[local_gov.lower()] = {}
        for indx in range(len(to_capture_df)):
            if to_capture_df["LGA"][indx].lower() == local_gov.lower():
                if to_capture_df["Ward"][indx] not in to_capture_dict[local_gov.lower()]:
                    to_capture_dict[local_gov.lower()][to_capture_df['Ward'][indx]] = []
                to_capture_dict[local_gov.lower()][to_capture_df['Ward'][indx]].append(to_capture_df["Settlement"][indx])
    return to_capture_dict, capture_list


