import pandas as pd
import re
import random


file_name = "2023_Kwara_P3B.xlsx"


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
    needed_sheets = [sheet for sheet in list_sheets if re.match(r'^[0-1]+', sheet) ]

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
    # print (df)
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
    new_data_frame = data_frame[columns]
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
