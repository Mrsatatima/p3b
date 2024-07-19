import pandas as pd
import openpyxl
import difflib
import os
from copy import deepcopy
import re


def write_rrcollect_csv(data_frame, write_csv=False):
    """
        a function that convert RR_Collect data to a format 
        suitable for matching process. It drops unwanted columns and splits 
        the coordinates field. It creates two csv files one for settlements
        and one for DH

        Args:
                Dataframe: pandas dataframe of the rr collect data set
        return:
                None

    """
    # fields ={
        # "State":"Please Select the State You are Currently In",
        # "LGA":"Please Select the LGA You are Currently In",
        # "Ward":"Please Select the ward",
        # "Type":"Is your current location a Settlement or a Distribution Hub?",
        # "Name of Settlement":"Please select the name of the settlement",
        # "DH":"What Distribution Hub is the settlement Clustered in?",
        # "Type of DH":"What type of Distribution Hub is this?",
        # "Others":"If others, please specify:",
        # "Name of DH":"Please enter the name of the Distribution hub",
        # "Settlement":"Please select the settlement the Distribution hub is located in",
        # "Location":"Capture the GPS Coordinate of the Location",
        # "Date_time":"Form Filling End"
        # }
    fields ={
        "State":"state",
        'Cluster':'cluster',
        'Supervisor':"supervisor",
        "Enumerator":"enumerator",
        "LGA":"lga",
        "Ward":"ward",
        "Type":"datatype",
        "Name of Settlement":"settlement_label",
        "ID":"settlement",
        "hf_ID":"settlement",
        "poi_ID":"settlement",
        "HF":"What Distribution Hub is the settlement Clustered in?",
        "Type of DH":"What type of Distribution Hub is this?",
        "Others set":"settlement_other",
        "Others HF": "hf_other",
        "Name of HF":"hf_name",
        "POI name": "poi_group-poiname",
        "Start_lat":"start-geopoint-Latitude",
        "Start_lon":"start-geopoint-Longitude",
        "End_lat":"geopoint-Latitude",
        "End_lon":"geopoint-Longitude",
        "Start_time":"start",
        "End_time":"start",
        }
    # settlement_data = {"State":[],"LGA":[],"Ward":[], "Name of Settlement":[],"DH":[],
                    #     "Latitude":[],"Longitude":[], "Acurracy":[], "Altitude":[],"Date_time":[]
                    # }
    settlement_data ={
        "State":[],
        'Cluster':[],
        'Supervisor':[],
        "Enumerator":[],
        "LGA":[],
        "Ward":[],
        "ID":[],
        "Name of Settlement":[],
        "Start_lat":[],
        "Start_lon":[],
        "End_lat":[],
        "End_lon":[],
        "Start_time":[],
        "End_time":[],
        }
    HF_data = {
        "State":[],
        'Cluster':[],
        'Supervisor':[],
        "Enumerator":[],
        "LGA":[],
        "Ward":[],
        "Name of Settlement":[],
        "Name of HF":[],
        "Start_lat":[],
        "Start_lon":[],
        "End_lat":[],
        "End_lon":[],
        "Start_time":[],
        "End_time":[],
        }
    POI_data ={
        "State":[],
        'Cluster':[],
        'Supervisor':[],
        "Enumerator":[],
        "LGA":[],
        "Ward":[],
        "Name of Settlement":[],
        # "Type":[],
        "POI name": [],
        "Start_lat":[],
        "Start_lon":[],
        "End_lat":[],
        "End_lon":[],
        "Start_time":[],
        "End_time":[],
        }
    # DH_data = {"State":[],"LGA":[],"Ward":[], "Settlement":[], "Name of DH":[], "Type of DH":[],
                    #     "Latitude":[],"Longitude":[], "Acurracy":[], "Altitude":[],"Date_time":[]
                    # }
    for idx in range(len(data_frame)):
        settlement = data_frame[fields["Name of Settlement"]][idx] if str(data_frame[fields["Name of Settlement"]][idx]) not in ["NAN","nan",""," ","0",0,] else data_frame[fields["Others set"]][idx]

        if data_frame[fields["Type"]][idx] == "poi":
            POI_data["State"].append(data_frame[fields["State"]][idx])
            POI_data["Cluster"].append(data_frame[fields["Cluster"]][idx])
            POI_data["LGA"].append(data_frame[fields["LGA"]][idx])
            POI_data["Ward"].append(data_frame[fields["Ward"]][idx])
            POI_data["Enumerator"].append(data_frame[fields["Enumerator"]][idx])
            POI_data["Supervisor"].append(data_frame[fields["Supervisor"]][idx])
            POI_data["Name of Settlement"].append(settlement)
            POI_data["POI name"].append(data_frame[fields["POI name"]][idx])
            # POI_data["Type"].append(type_of_dh)
            POI_data["Start_lat"].append(data_frame[fields["Start_lat"]][idx])
            POI_data["Start_lon"].append(data_frame[fields["Start_lon"]][idx])
            POI_data["End_lat"].append(data_frame[fields["End_lat"]][idx])
            POI_data["End_lon"].append(data_frame[fields["End_lon"]][idx])
            POI_data["End_time"].append(data_frame[fields["End_time"]][idx])
            POI_data["Start_time"].append(data_frame[fields["Start_time"]][idx])
        elif data_frame[fields["Type"]][idx] == "health_facility":
            hf = data_frame[fields["Name of HF"]][idx] if str(data_frame[fields["Name of HF"]][idx]) not in ["NAN","nan",""," ","0",0,] else data_frame[fields["Others HF"]][idx]

            HF_data["State"].append(data_frame[fields["State"]][idx])
            HF_data["Cluster"].append(data_frame[fields["Cluster"]][idx])
            HF_data["LGA"].append(data_frame[fields["LGA"]][idx])
            HF_data["Ward"].append(data_frame[fields["Ward"]][idx])
            HF_data["Enumerator"].append(data_frame[fields["Enumerator"]][idx])
            HF_data["Supervisor"].append(data_frame[fields["Supervisor"]][idx])
            HF_data["Name of Settlement"].append(settlement)
            HF_data["Name of HF"].append(hf)
            # HF_data["Type"].append(type_of_dh)
            HF_data["Start_lat"].append(data_frame[fields["Start_lat"]][idx])
            HF_data["Start_lon"].append(data_frame[fields["Start_lon"]][idx])
            HF_data["End_lat"].append(data_frame[fields["End_lat"]][idx])
            HF_data["End_lon"].append(data_frame[fields["End_lon"]][idx])
            HF_data["End_time"].append(data_frame[fields["End_time"]][idx])
            HF_data["Start_time"].append(data_frame[fields["Start_time"]][idx])                            
        else:
            settlement_data["State"].append(data_frame[fields["State"]][idx])
            settlement_data["Cluster"].append(data_frame[fields["Cluster"]][idx])
            settlement_data["Supervisor"].append(data_frame[fields["Supervisor"]][idx])
            settlement_data["Enumerator"].append(data_frame[fields["Enumerator"]][idx])
            settlement_data["LGA"].append(data_frame[fields["LGA"]][idx])
            settlement_data["Ward"].append(data_frame[fields["Ward"]][idx])
            settlement_data["Name of Settlement"].append(settlement)
            settlement_data["ID"].append(data_frame[fields["ID"]][idx])
            settlement_data["Start_lat"].append(data_frame[fields["Start_lat"]][idx])
            settlement_data["Start_lon"].append(data_frame[fields["Start_lon"]][idx])
            settlement_data["End_lat"].append(data_frame[fields["End_lat"]][idx])
            settlement_data["End_lon"].append(data_frame[fields["End_lon"]][idx])
            settlement_data["End_time"].append(data_frame[fields["End_time"]][idx])
            settlement_data["Start_time"].append(data_frame[fields["Start_time"]][idx])  
   
    settlement_dataframe = pd.DataFrame(settlement_data, index=None)
    poi_dataframe = pd.DataFrame(POI_data, index=None)
    hf_dataframe = pd.DataFrame(HF_data, index=None)
    if write_csv:
        settlement_file_name = os.getcwd()+"\\"+"Cleaned_settlement_capture.csv"
        hf_file_name = os.getcwd()+"\\"+"Cleaned_adamawa_hf_capture.csv"
        poi_file_name = os.getcwd()+"\\"+"Cleaned_adamawa_poi_capture.csv"
        settlement_dataframe.to_csv(settlement_file_name, index=False)
        hf_dataframe.to_csv(hf_file_name, index=False)
        poi_dataframe.to_csv(poi_file_name, index=False)

        return settlement_file_name, hf_file_name, poi_file_name

    return settlement_dataframe, hf_dataframe, poi_dataframe


def write_grid3_csv(data_frame, state, write_csv=False):
    """
        extracts all settlments points of a state from the GRID3 data sets.
        it arrange the columns in a format suitable for matching process
        Args:
                data_frame: pandas dataframe of the GRID3 settlement point
                            data 
                state: The state you want it settlements to be extracted
    """
    settlement_data = {"State":[],"LGA":[],"Ward":[], "Name of Settlement":[],
                        "Latitude":[],"Longitude":[],}
    for idx in range(len(data_frame)):
        if data_frame['statename'][idx] == f"{state}":
            settlement_data["State"].append(data_frame["statename"][idx])
            settlement_data["LGA"].append(data_frame["lganame"][idx])
            settlement_data["Ward"].append(data_frame["wardname"][idx])
            settlement_data["Name of Settlement"].append(data_frame["set_name"][idx])
            settlement_data["Latitude"].append(data_frame["Y"][idx])
            settlement_data["Longitude"].append(data_frame["X"][idx])
          

    settlement_dataframe = pd.DataFrame(settlement_data, index=None)
    if write_csv:
        settlement_dataframe.to_csv(f"{state}_grid3_settlements.csv", index=False)
    return settlement_dataframe


def get_p3b_list(df, LGA):
    """
        Extracts a list of settlements from a DataFrame containing P3B information.

        Input:
            df : The DataFrame containing the P3B information(pandas.DataFrame)
            LGA : The name of the Local Government Area (LGA) to extract 
                settlements from (str).
            p3b : Indicates whether the Dataframe is a P3B or not (bool).

        Outputs:
            tuple: A tuple containing the extracted settlements 
                (as a dictionary) and the number of settlements found.
     """

    # Initialize an empty dictionary to store the extracted data
    p3b_list = {}

    # Initialize a counter variable to keep track of the number of settlements
   
    # Iterate over each row of the DataFrame
    for idx in range(len(df)):
        # Extract the settlement information from the appropriate column based on the p3b parameter
        if not re.match(r'^nan', str(df['List of contiguous communities/ settlements'][idx]), re.IGNORECASE)\
            and not str(df['List of contiguous communities/ settlements'][idx]).isdigit():
            settlement = " ".join(str(df['List of contiguous communities/ settlements' ][idx]).lower().replace(".", "").replace(".", "").replace(")", "").replace("(", "").strip().split())
            
            # Extract the LGA information from the input parameter
            lga = f"{LGA}".lower().strip()

            # Extract the ward information from the appropriate column based on the p3b parameter
            ward = str(df['Wards'][idx]).lower().strip()

            # Add the settlement information to the p3b_list dictionary
            if lga not in p3b_list:
                p3b_list[lga] = {}
            if ward not in p3b_list[lga]:
                p3b_list[lga][ward] = set()
            if settlement != "nan" and str(df['List of contiguous communities/ settlements'][idx]) not in ["", " ", "Nan", "NAN", "nan", "0", 0]:
                p3b_list[lga][ward].add(settlement)

    # Sort the settlements in each ward by name
    for key, values in p3b_list[LGA.lower()].items():
        p3b_list[LGA.lower()][key] = sorted(values)

    # Return the p3b_list dictionary and the settlement count
    return p3b_list


def get_captured_list(df, LGA, lga_dict, captured_list = {}, grid3=False):

    """
        Returns a dictionary of captured settlements in a given Local Government Area
        (LGA) with their corresponding coordinates.

        Args:
        df (pandas DataFrame): The data containing settlement, LGA, ward, latitude, 
                                longitude, and, if grid3 is False, altitude and accuracy.
        LGA (str): The name of the Local Government Area.
        grid3 (bool, optional): A boolean indicating whether to include altitude and accuracy 
                                values in the output. Defaults to False. It salso indicates 
                                whether the file is RR_colect or grid3 dataset

        Returns:
        dict: A dictionary where keys are LGAs and values are dictionaries where keys are wards and values are dictionaries
             where keys are settlements and values are strings of latitude and longitude separated by a '|' character, or, if grid3 is True, separated by '|' and followed by altitude and accuracy separated by '|'.

    """
    

    # Iterate over each row in the dataframe
    for idx in range(len(df)):
        # Get the name of the settlement, LGA, ward, latitude, and longitude
        settlement = " ".join(str(df["Name of Settlement"][idx]).lower().replace(".","").replace(".","").replace(")","").replace("(","").strip().split())
        lga = str(df["LGA"][idx]).lower().strip()
        ward = str(df["Ward"][idx]).lower().strip()
        latitude= str(df["Latitude"][idx]).lower().strip()
        longitude = str(df["Longitude"][idx]).lower().strip()

        # If grid3 is False, also get the accuracy and altitude values
        if not grid3:
            accuracy = str(df["Acurracy"][idx]).lower().strip()
            altitude = str(df["Altitude"][idx]).lower().strip()
        if grid3:
            LGA = lga_dict[LGA.lower()].lower()
        
        # If the LGA matches the requested LGA
        if lga == LGA.lower():#LGA.lower():
            # Add the settlement to the captured_list dictionary
            if lga not in captured_list:
                captured_list[lga] = {}
            if ward not in captured_list[lga]:
                captured_list[lga][ward] = {}
            if settlement not in captured_list[lga][ward]:
                # If grid3 is False, only add latitude and longitude to the captured_list value
                captured_list[lga][ward][settlement] = f"{latitude}|{longitude}" if grid3 else f"{latitude}|{longitude}|{accuracy}|{altitude}"

    return captured_list


def matching_same_name(p3b_list, capture_list, perfect_match, LGA, lga_dict, ward_dict, captured=True):
    """
        Matches settlements in the P3B list with those in the capture list that have the same name, 
        and returns a dictionary of perfect matches. 
        
        Args:
            p3b_list (dict): Dictionary of settlements in P3B list.
            capture_list (dict): Dictionary of captured settlements.
            perfect_match (dict): Dictionary of perfect matches.
            LGA (str): Name of Local Government Area.
            captured (bool): Whether the capture list is a RR collect or a GRID3 list. 
                Defaults to True.
        
        Returns:
            tuple: A tuple containing the updated P3B list, capture list, perfect match dictionary, and count of matches.
    """
    settlement_list = {}
    count = 0
    
    # Iterate through the P3B list and compare settlements to the captured settlements.
    for lga, wards in p3b_list.items():
        if lga_dict[lga] in capture_list:
            for ward in wards:
               
                # print(ward,com_ward_dict[lga][ward])
                if ward_dict[lga][ward] in capture_list[lga_dict[lga]]:
                    for settlement in wards[ward]:
                        if settlement in capture_list[lga_dict[lga]][ward_dict[lga][ward]]:
                            # Add the settlement to the perfect match dictionary.
                            if lga not in perfect_match:
                                perfect_match[lga] = {}
                            if ward not in perfect_match[lga]:
                                perfect_match[lga][ward] = {}
                            perfect_match[lga][ward][settlement] = {settlement: capture_list[lga_dict[lga]][ward_dict[lga][ward]][settlement]} \
                                if captured else {settlement: settlement}
                            count += 1
                            
                            # Remove the settlement from the capture list.
                            if captured:
                                capture_list[lga_dict[lga]][ward_dict[lga][ward]].pop(settlement)
                            else:
                                capture_list[lga_dict[lga]][ward_dict[lga][ward]].pop(settlement)
                            
                            # Add the settlement to the settlement list.

                            if ward not in settlement_list:
                                settlement_list[ward] = []
                            settlement_list[ward].append(settlement)
    
    # Remove settlements from the P3B list that have been matched using the settlement list.
    # for lg in LGA:
    
    for ward, settlements in settlement_list.items():
        for settlement in settlements:
            if ward in p3b_list[LGA.lower()]:
                if settlement in p3b_list[LGA.lower()][ward]:
                    p3b_list[LGA.lower()][ward].remove(settlement)
    
    # Return the updated P3B list, capture list, perfect match dictionary, and count of matches.
    return p3b_list, capture_list, perfect_match, count


def match_phrases(phrase1, phrase2, ratio=0.8):
    """
        Compares two phrases and returns whether they are a match based on a similarity ratio.

        Args:
            phrase1 (str): The first phrase to compare.
            phrase2 (str): The second phrase to compare.
            ratio (float, optional): The minimum similarity ratio required to consider the phrases a match. Defaults to 0.8.

        Returns:
            tuple: A tuple containing a boolean indicating whether the phrases are a match, and the similarity ratio between them.
    """
    # If either phrase is empty or only contains whitespace, they cannot be a match
    if phrase1 in [" ",""] or phrase2 in [" ",""]:
        return False, 0
    
    # Calculate the similarity ratio between the two phrases using the SequenceMatcher class from difflib
    similarity_ratio = difflib.SequenceMatcher(None, phrase1, phrase2).ratio()
    
    # If the similarity ratio is above the specified threshold, consider the phrases a match
    if similarity_ratio >= ratio:  
        return True, similarity_ratio
    else:
        return False, similarity_ratio


def similar_name(p3b_list, capture_list, perfect_match, LGA, ratio, lga_dict, ward_dict, dictionary=False):
    """
        Find similar names between two dictionaries of settlements.

        Parameters:
        -----------
        p3b_list : dict
            A dictionary of settlements with Local Government Areas and wards as keys from P3B.
        capture_list : dict
            A dictionary of settlements with Local Government Areas and wards as keys from RR Collect of GRID3.
        perfect_match : dict
            A dictionary to store the matching settlements.
        LGA : str
            A string that specifies the Local Government Area to match.
        ratio : float
            A float between 0 and 1 that specifies the ratio of similarity between the settlement names.
        captured : bool, optional
            A boolean value that specifies if the settlement name should be captured or not.
        dictionary : bool, optional
            A boolean value that specifies if the common words in the settlement names should be removed.

        Returns:
        --------
        tuple
            A tuple containing four elements:
            - A dictionary of matching settlements.
            - A dictionary of settlements with unmatched settlements removed.
            - The number of settlements removed.
            - A dictionary of settlements that did not match.
    """
    p3b_list=deepcopy(p3b_list)  # Make a copy of p3b_list to avoid modifying the original
    capture_list=deepcopy(capture_list)  # Make a copy of capture_list to avoid modifying the original
    count =0  # Initialize a count variable to zero
    settlement_list = {}  # Create an empty dictionary to store the settlement data

    # Loop through the LGA and wards in p3b_list
    for lga, wards in p3b_list.items():
        if lga_dict[lga] in capture_list:  # Check if the LGA is in the capture_list or matching
            # Loop through the wards in the p3b_list
            for ward in wards:
                if ward_dict[lga][ward] in capture_list[lga_dict[lga]]:  # Check if the ward is in the capture_list for the current LGA
                    # Loop through the settlements in the current ward
                    for settlement in wards[ward]:
                        matcthin_list = {}  # Initialize an empty dictionary to store matching settlements

                        # Loop through the settlements in the capture_list for the current LGA and ward
                        for settlement2 in capture_list[lga_dict[lga]][ward_dict[lga][ward]]:
                            common_words = ["anguwan","anguwar","anguwa","angwa","ang","unguwan","unguwar","unguwa"
                                            "alhaji","alh", "gidan","gildan","jauro","ung","g/","gida","gidan",
                                            "c/garin",'c/garin',"c/", "cikin","garin","village","head","mallam","malam",
                                            "primary", "secondary","hospital","dh","sec","line","street","str",
                                            "s/garin","sabon gari","sabongari","gari","k/","kauyen","kauye","katangar",
                                            "settlement","road","rd","town","street","str"]  # Define a list of common words to remove from settlement names
                            common_words.append(lga)
                            settlement_remove = settlement  # Set the settlement_remove variable to the current settlement
                            settlement2_remove = settlement2  # Set the settlement2_remove variable to the current settlement in the capture_list
                            if dictionary: # if dictionary is true remove common words
                                for word in common_words: # loop through common_words list
                                    settlement_remove = settlement_remove.replace(word,"") # remove common words from settlement
                                    settlement2_remove = settlement2_remove.replace(word,"") # remove common words from settlement2
                            settlement2_remove.strip() # remove leading/trailing spaces from settlement2_remove
                            settlement_remove.strip() # remove leading/trailing spaces from settlement_remove
                            get_match = match_phrases(settlement_remove,settlement2_remove,ratio) # get match between settlement and settlement2
                            if get_match[0]: # if get_match is is true
                                matcthin_list[settlement2] = get_match[1] # add settlement2 and its match ratio to matcthin_list
                        if matcthin_list: # if matcthin_list is not empty
                            settlement2 = max(matcthin_list, key=matcthin_list.get) # get settlement2 with highest match ratio
                            count+=1
                            if lga not in perfect_match: # if lga not in perfect_match
                                perfect_match[lga]={} # add lga to perfect_match
                            if ward not in perfect_match[lga]: # if ward not in perfect_match[lga]
                                perfect_match[lga][ward]={} # add ward to perfect_match[lga]
                            if settlement not in perfect_match[lga][ward]: # if settlement not in perfect_match[lga][ward]
                                perfect_match[lga][ward][settlement]={} # add settlement to perfect_match[lga][ward]
                            perfect_match[lga][ward][settlement][settlement2]=capture_list[lga_dict[lga]][ward_dict[lga][ward]][settlement2] 
                            # add settlement and its best match (settlement2) to perfect_match[lga][ward]
                            capture_list[lga_dict[lga]][ward_dict[lga][ward]].pop(settlement2) # remove settlement2 from capture_list
                            if ward not in settlement_list: # if ward not in settlement_list
                                settlement_list[ward] =set() # add ward to settlement_list
                            settlement_list[ward].add(settlement) # add settlement to settlement_list[ward]

    # loop through settlement_list to remove settlements that are matched in p3b_list
    # for lg in LGA:
    for ward, settlements in settlement_list.items():
        for settlement in settlements:
            if ward in p3b_list[LGA.lower()]:
                if settlement in p3b_list[LGA.lower()][ward]:
                    p3b_list[LGA.lower()][ward].remove(settlement)
    # return the following variables
    return perfect_match, p3b_list, count, capture_list

def create_final_data_frame(matched_settlements, unmatched_settlements, grid3=False,field_name="GRID3 Name"):
    """
        Creates an excel sheet with settlement data for a given Local Government Area (LGA).

        Args:
            matched_settlements (dict): A dictionary containing matched settlements information.
            unmatched_settlements (dict): A dictionary containing unmatched settlements information.
            LGA (str): Name of the Local Government Area (LGA).
            file_name (str): Name of the Excel file to be created.
            grid3 (bool, optional): A boolean value indicating whether its GRID3 or RR Collect.
                                    Defaults to False.
            field_name (str, optional): Name of the field to be used for Grid3 name if grid3 is True.
                                        Defaults to "GRID3 Name".

        Returns:
            str: A string indicating that the function has finished execution ("DONE").
    """

    lga_name = []
    ward_name =[]
    p3b_name = []
    grid3_name = []
    capture_name= []
    coordinate = []
    lat  =[]
    lon = []
    acc = []
    alt = []

    # Loop through the matched_settlements dictionary to extract information
    # and append it to respective lists
    for lga, wards in matched_settlements.items():
        for ward, dhs in wards.items():
            for dh, dh2 in dhs.items():
                text =""
                cod_text =""
                for name, coord in dh2.items():
                    text += f"{name}"
                    cod_text += f"{coord}"
                cod =cod_text.split("|")
                lat.append(cod[0])
                lon.append(cod[1])
                if len(cod) ==4:
                    acc.append(cod[2])
                    alt.append(cod[3])
                else:
                    acc.append("")
                    alt.append("")

                capture_name.append(text.capitalize())
                lga_name.append(lga.capitalize())
                ward_name.append(ward.capitalize())
                p3b_name.append(dh.capitalize())

    # Loop through the unmatched_settlements dictionary to extract information
    # and append it to respective lists
    for lga, wards in unmatched_settlements.items():
        for ward, dhs in wards.items():
            for dh in dhs:
                coordinate.append("")
                grid3_name.append(" ")
                capture_name.append(" ")
                lga_name.append(lga.capitalize())
                ward_name.append(ward.capitalize())
                p3b_name.append(dh)
                lat.append("")
                lon.append("")
                acc.append("")
                alt.append("")

    # Create pre_reconciled DataFrame with the extracted information
    if not grid3:
        pre_reconciled = pd.DataFrame({"LGA":lga_name,"Ward":ward_name,"DH P3B Name":p3b_name,
                            f"{field_name}":capture_name, "Latitude":lat,"Longitude":lon,
                            "Accuracy":acc,"Altitude":alt})
    else:
        pre_reconciled = pd.DataFrame({"LGA":lga_name,"Ward":ward_name,"DH P3B Name":p3b_name,
                            f"{field_name}":capture_name, "Latitude":lat,"Longitude":lon,})

    # Print pre_reconciled DataFrame
    print(pre_reconciled)
   
    return pre_reconciled
