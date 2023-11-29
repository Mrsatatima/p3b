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
