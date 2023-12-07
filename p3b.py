
import pandas as pd
import re
import os
import openpyxl


def get_sheet_helper(file_name, sheet):
    """
        this is a helper function for get sheets
        it get sheets of lga of P3b template that
        did not follow the name format of "number.lga_name 
        i.e "1.Asa"
        Input:
            filename: path to the p3b template (str)
            sheets: List of all the sheets in the p3b template file (list)
        Ouput:
            new_sheets: a list of all valid sheets (sheet of lga only) (list)
    """
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


def populate_wards(data_frame):
    """
        this function populates the cells on the ward column with respective
        ward names, its assign a ward to each settlement since on the p3b
        template the ward column is a merged column
        Input:
            data_frame: it take a cleaned p3b data frame with actual header
                        and first blank column removed (pandas dataframe)
        Output:
            data_frame: a data frame with wards populated for each 
                        settlement (pandas dataframe)
    """
    group = []
    ward = ""
    for idx in range(len(data_frame)):
        if not re.match(r'^nan', str(data_frame['Wards'][idx]), re.IGNORECASE):
            if not re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
                ward = data_frame['Wards'][idx]
        if not re.match(r'^nan', str(data_frame['List of contiguous communities/ settlements'][idx]), re.IGNORECASE):
            if not re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
                group.append(idx)
        if re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
            if ward != "" and len(group) != 0:
                for i in group:
                    data_frame.loc[i, ['Wards']] = ward
                ward = ""
                group = []
    return data_frame


def populate_dh(data_frame):
    """
        this function populates the cells on the dh column with respective
        dh names, its assign a dh to each settlement since on the p3b
        template the settlements are grouped per DH but the name of 
        the dh is only on the settlment it is located in
        Input:
            data_frame: it take a cleaned p3b data frame with actual header
                        and first blank column removed and wards being 
                        populated(pandas dataframe)
        Output:
            data_frame: a data frame with dh populated for each
                        settlement (pandas dataframe)
    """
    group = []
    dh = ""
    for idx in range(len(data_frame)):
        if not re.match(r'^nan', str(data_frame['Wards'][idx]), re.IGNORECASE):
            if not re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
                if not re.match(r'^nan', str(data_frame['Name of DH'][idx]), re.IGNORECASE):
                    dh = data_frame['Name of DH'][idx]
        if not re.match(r'^nan', str(data_frame['List of contiguous communities/ settlements'][idx]), re.IGNORECASE):
            if not re.match(r'^sub\s*total\s*$', str(data_frame['Wards'][idx]), re.IGNORECASE):
                group.append(idx)
        if re.match(r'^nan', str(data_frame['List of contiguous communities/ settlements'][idx]), re.IGNORECASE):
            if dh != "" and len(group) != 0:
                for i in group:
                    data_frame.loc[i, ['Name of DH']] = dh
                dh = ""
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
        data_frame.fillna("")
        data_frame.to_excel(writer, sheet_name, index=False)
    # writer.close()
    return "DONE"


def get_lga_name(sheet):
    """
        this cleans sheet name to be just an lga name
        that can be used is procesiing
        Input:
            sheet: Sheet name (str)
        Output:
            lga: clean lga name (str)
    """
    lga_list = sheet.split('.')
    try:
        lga = lga_list[1].strip().lower().title()
    except:
        lga = lga_list[0].strip().lower().title()
    return lga