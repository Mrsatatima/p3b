import pandas as pd
import re
import os
import openpyxl


from geo_script import *


def get_sheet_helper(file_name, sheet):
    new_sheet = []
    for s in sheet:
        df = pd.read_excel(file_name, sheet_name=s)
        cols =df.columns
        # print(cols)
        for col in cols:
            if re.match(r'^20[0-9]{2}\s*ITN\s*MASS\s*CAMPAIGN\s*[-]\s*', str(col), re.IGNORECASE):
                # print(col)
                new_sheet.append(s)
                break
    return new_sheet

def get_sheets(file_name):
    """
        this function gathers all the list of sheet needed for 
        p3b data cleaning
        Input:
        file_name: Name of the P3B excel file (str)
        Output:
        needed_sheets: list of sheets needed (list)
    """
    excel_file = pd.ExcelFile(file_name)
    list_sheets = excel_file.sheet_names
    needed_sheets = [sheet for sheet in list_sheets if re.match(r'^[0-9]+[.]?', sheet)]
    if len(needed_sheets) == 0:
        return get_sheet_helper(file_name,list_sheets)
    excel_file.close()

    return needed_sheets


def actual_header_row(data_frame):
    """
        this function gets the indx of the actual column headers 
        in th P3B template
        Input:
        data_frame: Data frame of the P3B template (pandas data frame)
        Output:
        idx: Index of the row of the for the column headers (integer)
    """
    for idx in range(len(data_frame.iloc[:,1].head(20))):
        txt = data_frame.iloc[:,1][idx]
        if re.match(r'((serial)|(s)|(s))\s?/?\s?((number)|(num)|(no)|(n))[.]?',
                    str(txt), re.IGNORECASE):
            return idx


def remove_first_blank_column(file, row_index, sheet):
    """
        this removes the first blank column on the P3B 
        and it also set the actual headers for the columns
        Input:
        file: The name of the p3b file (str)
        row_index: the index of the row you wish to make the 
                    header (int)
        sheet: Name of the sheet you want to access (str)
        Output:
        df: A data frame of p3b with actual header an deleted
            blank column (pandas dataframe)
    """
    df = pd.read_excel(file, sheet_name=sheet, header=row_index)
    df = df.drop(df.columns[0], axis=1)
    headers = df.iloc[0]
    df.columns = headers
    df = df.drop(0)
    df = df.reset_index(drop=True)
    return df


def remove_unwanted_columns(data_frame, columns):
    """
        this function removes all unwanted columns
        and create a dataframe consisting of only
        columns of interest
        Input
        data_frame: dataframe that needs to be formatted (pandas dataframe)
        columns: list of columns of interest (list)
        Output:
        new_data_frame: A formatted dataframe with only columns of interest
                        (pandas dataframe)
    """
    needed_column_data_frame = data_frame[columns]
    new_column_names = {columns[0]: "Wards", columns[1]: "Settlements",
                        columns[2]: "Population"}
    new_data_frame = needed_column_data_frame.copy()
    new_data_frame.rename(columns=new_column_names, inplace=True)
    return new_data_frame


def remove_blank_wards_rows(data_frame):
    """
        this function removes blank wards rows
        Input
        data_frame: dataframe to be formated
        Output
        data_frame: cleanded version of the input
    """
    for indx in range(len(data_frame)):
        if re.match(r'^nan', str(data_frame["Wards"][indx]),re.IGNORECASE):
            data_frame=data_frame.drop(indx)
    data_frame = data_frame.reset_index(drop=True)
    return data_frame


def remove_unsecured_wards(data_frame, list_wards):
    """
        this function removes wards rows of wards with security
        challenge
        Input:
            data_frame: dataframe to be formated (pandas dataframe)
            list_wards: list of wards with security challenge (list)
        Output:
        data_frame: cleanded version of the input (pandas dataframe)
    """
    for indx in range(len(data_frame)):
        if str(data_frame["Wards"][indx]) in list_wards:
            data_frame = data_frame.drop(indx)
    data_frame = data_frame.reset_index(drop=True)
    return data_frame


def drop_subtotal_rows(data_frame, ward_list):
    """
        this function takes a cleaned p3b data cleaned
        using the remo_unwanted_columns and remove_blank_wards_row
        and remove the subtotal rows while taking the values of total 
        population and total communities and add them to repective ward rows.
        The fucntion also removes wards that are security challenged
        it also adds a column for cumulative frequency
        Input:
            dataframe: Cleaned p3b data (pandas data frame)
            ward_list: list of wards with security challenge (list)
        Ouput:
            new_wards_df: a dataframe with list of wards and their respctive total
                    communities, total population and cumulative frequency
                    (pandas dataframe)
    """
    subtotal_df = data_frame
    wards_df = data_frame
    for indx in range(len(data_frame)):
        if data_frame["Wards"][indx] == "sub total":
            wards_df = wards_df.drop(indx)
        else:
            subtotal_df = subtotal_df.drop(indx)
    wards_df = wards_df.reset_index(drop=True)
    subtotal_df = subtotal_df.reset_index(drop=True)

    for indx in range(len(wards_df)):
        # wards_df["Wards"][indx]=subtotal_df["Wards"][indx]
        total_com = subtotal_df["Settlements"][indx]
        population = subtotal_df["Population"][indx]
        wards_df["Settlements"][indx] = total_com
        wards_df["Population"][indx] = population
    wards_df = wards_df.sort_values(by='Population')
    wards_df = wards_df.reset_index(drop=True)
    new_wards_df = remove_unsecured_wards(wards_df, ward_list)
    new_wards_df["Cumulative frequency"] = new_wards_df['Population'].cumsum()
    return new_wards_df


def create_random_cluster(data_frame, state, lga, lga_dct, ward_dct, clusters = 8):
    """
        this function takes in dataframe created using the drop_subtotal_rows
        its uses the cumulative frequency columns to create random clusters
        a new data is created columns of Wards, Total communities, Population
        cumulative frequency and cluster name
        Input
        data_frame: cleanded p3b data (pandas dataframe)
        clusters: defaults to 8, how many clusters you wish to create (int)
        Output:
        final_dif: Dataframe with clusters (pandas dataframe)
    """
    sum_population = data_frame['Population'].sum()
    population_interval = sum_population//clusters
    start_random = random.choice(range(1000, 2000))
    step_random = random.choice(range(100, 300))
    start_range = random.choice(range(abs(int(data_frame["Cumulative frequency"][0])-1000),(int(data_frame["Cumulative frequency"][0])+1000),500))
    start_population = random.choice(range(start_random, start_range, step_random))
    pop_list = []
    for indx in range(clusters):
        pop_list.append(start_population)
        start_population = start_population+population_interval
        data = {"Wards": [], "Total communities": [], "Population": [],
                "Cumulative frequency": [], "Clusters": [],"XY Coordinates":[],
                "Direction URL":[]}
    final_df = pd.DataFrame(data)
    
    for i, population in enumerate(pop_list):
        for indx in range(len(data_frame)):
            if population <= data_frame["Cumulative frequency"][indx]:
                ward = data_frame["Wards"][indx]
                com = data_frame["Settlements"][indx]
                pop = data_frame["Population"][indx]
                cum = data_frame["Cumulative frequency"][indx]
                cluster = f"Cluster {i+1} ({population})"
                location = geo_location(wards_shapefile, set_extent_shapefile, state, lga, ward,lga_dct,ward_dct)
                xy_coordinates = f'{location[0]}|{location[1]}'
                url = f"https://www.google.com/maps/dir/'8.456104,4.544522'/{location[1]},{location[0]}"
                data = {"Wards": [ward], "Total communities": [com],
                        "Population": [pop], "Cumulative frequency": [cum],
                        "Clusters": [cluster],"XY Coordinates":[xy_coordinates],
                        "Direction URL":[url]}
                new_row = pd.DataFrame(data)
                final_df = pd.concat([final_df, new_row], ignore_index=True)
                break
            continue
    return final_df


def populate_wards(data_frame):
    for idx in range(len(data_frame)):
        if not re.match(r'^nan', str(data_frame['Wards'][idx]),re.IGNORECASE):
            if not re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
                ward = data_frame['Wards'][idx]
        if not re.match(r'^nan', str(data_frame['List of contiguous communities/ settlements'][idx]),re.IGNORECASE):
            if not re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
                group.append(idx)
        # print(str(data_frame['Wards'][idx]))
        if re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
            # print(ward, group)
            if ward != "" and len(group) != 0:
                print(group, ward)
                for ix in group:
                    data_frame.loc[ix,['Wards']]= ward
                ward =""
                group = []
    return data_frame
    

def write_to_excel(data_frame, file_name, sheet_name):
    """
        this function writes a sheet to an existing workbook
        if the workbook does not exist it creates the workbook
        and write a sheet to it
        Input:
        data_frame: the pandas dataframe you want to write to a workbook
                   (pandas dataframe)
        file_name: name of the workbook you wish to write to (str)
        sheet_name: name of sheet (str)
    """
    # create excel file using file name if its not in the directory
    if not os.path.isfile(file_name):
        wb = openpyxl.Workbook()  
        wb.save(file_name)
    # Open the workbook and create a writer object to write the DataFrame to the sheet
    # work_book = openpyxl.load_workbook(file_name, data_only=True)
    with pd.ExcelWriter(file_name, "openpyxl", mode="a", if_sheet_exists='replace') as writer:
        # writer.book = work_book
        data_frame.to_excel(writer, sheet_name, index=False)
    # writer.close()
    return "DONE"


 