import pandas as pd
import openpyxl



def write_rrcollect_csv(data_frame):
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
    fields ={
        "State":"Please Select the State You are Currently In",
        "LGA":"Please Select the LGA You are Currently In",
        "Ward":"Please Select the ward",
        "Type":"Is your current location a Settlement or a Distribution Hub?",
        "Name of Settlement":"Please select the name of the settlement",
        "DH":"What Distribution Hub is the settlement Clustered in?",
        "Type of DH":"What type of Distribution Hub is this?",
        "Others":"If others, please specify:",
        "Name of DH":"Please enter the name of the Distribution hub",
        "Settlement":"Please select the settlement the Distribution hub is located in",
        "Location":"Capture the GPS Coordinate of the Location",
        "Date_time":"Form Filling End"
        }
    settlement_data = {"State":[],"LGA":[],"Ward":[], "Name of Settlement":[],"DH":[],
                        "Latitude":[],"Longitude":[], "Acurracy":[], "Altitude":[],"Date_time":[]
                    }
    DH_data = {"State":[],"LGA":[],"Ward":[], "Settlement":[], "Name of DH":[], "Type of DH":[],
                        "Latitude":[],"Longitude":[], "Acurracy":[], "Altitude":[],"Date_time":[]
                    }
    for idx in range(len(data_frame)):
        if data_frame[fields["Type"]][idx] == "Distribution Hub":
            DH_data["State"].append(data_frame[fields["State"]][idx])
            DH_data["LGA"].append(data_frame[fields["LGA"]][idx])
            DH_data["Ward"].append(data_frame[fields["Ward"]][idx])
            DH_data["Settlement"].append(data_frame[fields["Settlement"]][idx])

            DH_data["Name of DH"].append(data_frame[fields["Name of DH"]][idx])
            type_of_dh = data_frame[fields["Type of DH"]][idx] if data_frame[fields["Type of DH"]][idx] != "Other" else data_frame[fields["Others"]][idx]
            DH_data["Type of DH"].append(type_of_dh)
            DH_data["Acurracy"].append(data_frame[fields["Location"]][idx].split("|")[0])
            DH_data["Altitude"].append(data_frame[fields["Location"]][idx].split("|")[1])
            DH_data["Latitude"].append(data_frame[fields["Location"]][idx].split("|")[2])
            DH_data["Longitude"].append(data_frame[fields["Location"]][idx].split("|")[3])
            DH_data["Date_time"].append(data_frame[fields["Date_time"]][idx])
        else:
            settlement_data["State"].append(data_frame[fields["State"]][idx])
            settlement_data["LGA"].append(data_frame[fields["LGA"]][idx])
            settlement_data["Ward"].append(data_frame[fields["Ward"]][idx])
            settlement_data["Name of Settlement"].append(data_frame[fields["Name of Settlement"]][idx])
            settlement_data["DH"].append(data_frame[fields["DH"]][idx])
            settlement_data["Acurracy"].append(data_frame[fields["Location"]][idx].split("|")[0])
            settlement_data["Altitude"].append(data_frame[fields["Location"]][idx].split("|")[1])
            settlement_data["Latitude"].append(data_frame[fields["Location"]][idx].split("|")[2])
            settlement_data["Longitude"].append(data_frame[fields["Location"]][idx].split("|")[3])
            settlement_data["Date_time"].append(data_frame[fields["Date_time"]][idx])

    settlement_dataframe = pd.DataFrame(settlement_data, index=None)
    dh_dataframe = pd.DataFrame(DH_data, index=None)
    print(settlement_dataframe)
    print(dh_dataframe)
    settlement_dataframe.to_csv("Cleaned_adamawa_settlement_capture.csv", index=False)
    dh_dataframe.to_csv("Cleaned_adamawa_DH_capture.csv", index=False)
    return settlement_dataframe, dh_dataframe


def write_grid3_csv(data_frame,state):
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
        if str(df["List of contiguous communities/ settlements"][idx]) not in ["", " ", "NAN", "nan", "0"]\
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

def get_captured_list(df, LGA, lga_dict,grid3=False):

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
    captured_list = {}

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

        # If the LGA matches the requested LGA
        if lga == lga_dict[LGA.lower()].lower():#LGA.lower():
            # Add the settlement to the captured_list dictionary
            if lga not in captured_list:
                captured_list[lga] = {}
            if ward not in captured_list[lga]:
                captured_list[lga][ward] = {}
            if settlement not in captured_list[lga][ward]:
                # If grid3 is False, only add latitude and longitude to the captured_list value
                captured_list[lga][ward][settlement] = f"{latitude}|{longitude}" if grid3 else f"{latitude}|{longitude}|{accuracy}|{altitude}"

    return captured_list
