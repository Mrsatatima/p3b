import pandas as pd
from geo_script import *


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


def create_random_cluster(data_frame, state, lga, lga_dct, ward_dct, clusters= 8):
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


