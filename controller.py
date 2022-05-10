# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 19:45:21 2022

@author: keatin6
"""

# %%

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import upg_LightType, upg_PlantType, upg_Soil, upg_WateringType
from model import upg_PlantingMethod, upg_Category, upg_Bionomic
from model import OlvPlant, upg_Plant, upg_Subcategory

# %%

def connect_to_database():
    engine = create_engine("sqlite:///PlantingGuideDB.db", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# %%

def get_result(session):
    results = session.query(
        upg_PlantType, 
        upg_PlantType.PlantType, 
        upg_LightType.LightType
    ).join(
        upg_LightType,
        upg_LightType.LightTypeID == upg_PlantType.LightTypeID
    ).all()
    return results[0][1]

# %%

def table_routing(input_data):
    if input_data == "cat":
        table_to_query = upg_Category
    elif input_data == "sub":
        table_to_query = upg_Subcategory
    elif input_data == "plt":
        table_to_query = upg_PlantType
    elif input_data == "lgt":
        table_to_query = upg_LightType
    elif input_data == "soi":
        table_to_query = upg_Soil
    elif input_data == "wtr":
        table_to_query = upg_WateringType
    else:
        table_to_query = None
    return table_to_query

# %%

def find_id_from_value(session, table, value):
    result_dict = return_result_dict_from_table(session, table)
    try:
        result_id = result_dict[value]
    except:
        print(f"{value} is not found in {table.__tablename__}.")
        result_id = None
    return result_id

# %%

def return_result_dict_from_table(
        session, table, plant_type_filter=None, category_filter=None):
    #Query the inputted table
    results = session.query(
        table)
    #If a subcategory filter was specified filter results
    if plant_type_filter and table == upg_Subcategory:
        results = results.filter(
            table.PlantTypeID == plant_type_filter)
    #If a subcategory filter was specified filter results
    if category_filter and table == upg_PlantType:
        results = results.filter(
            table.CategoryID == category_filter)
    #Convert the results
    results = results.all()
    #Create a dict to store data
    result_dict = {}
    #Loop through results saving the IDs as values in a dict
    for result in results:
        id_field = str(result.ID)
        name_field = str(result.Name)
        result_dict[name_field] = id_field
    #Return the dict
    return result_dict

# %%

def convert_results_dict_to_list(result_dict):
    return list(result_dict.keys())

def get_combo_choices(
        session, table_code, plant_type_filter=None, category_filter=None):
    table = table_routing(table_code)
    results = return_result_dict_from_table(
        session, table, plant_type_filter, category_filter)
    result_list = convert_results_dict_to_list(results)
    return result_list


# %%


def split_day_range(range_string):
    if "-" in range_string:
        day_min, day_max = range_string.split("-")
        return day_min, day_max
    else:
        return None, None
    
def insert_plant_record(
        session, plant, subcategory_id, plant_type_id, 
        dtg_rng=None, dtm_rng=None):
    new_record = upg_Plant()
    new_record.PlantName = plant
    new_record.SubcategoryID = subcategory_id
    new_record.PlantTypeID = plant_type_id
    
    if dtg_rng:
        dtg_min, dtg_max = split_day_range(dtg_rng)
        if dtg_min and dtg_max:
            new_record.DTG_min = dtg_min
            new_record.DTG_max = dtg_max
    
    if dtm_rng:
        dtm_min, dtm_max = split_day_range(dtm_rng)
        if dtm_min and dtm_max:
            new_record.DTM_min = dtm_min
            new_record.DTM_max = dtm_max
    
    
    session.add(new_record)
    session.commit()
    
# %%



# %%

def convert_plant_results(plant_results):
    plant_list = []
    for plant_result in plant_results:
        category = plant_result[0]
        subcategory = plant_result[1]
        plant_type = plant_result[2]
        plant = plant_result[3]
        scientific = ""
        if plant_result[4] and plant_result[5]:
            scientific = plant_result[4]+' '+plant_result[5]
        plant = OlvPlant(
            category,
            subcategory,
            plant_type,
            plant,
            scientific)
        plant_list.append(plant)
    return plant_list
        

# %%


def get_plant_results(session):
    results = session.query(
        upg_Category.Name, 
        upg_Subcategory.Name,
        upg_PlantType.Name, 
        upg_Plant.PlantName, 
        upg_Bionomic.Genus, 
        upg_Bionomic.Species
    ).join(
        upg_PlantType,
        upg_PlantType.ID == upg_Plant.PlantTypeID
    ).join(
        upg_Category,
        upg_Category.ID == upg_PlantType.CategoryID
    ).outerjoin(
         upg_Bionomic,
         upg_Bionomic.ScientificID == upg_Plant.ScientificID
    ).join(
        upg_Subcategory,
        upg_Subcategory.ID == upg_Plant.SubcategoryID
    ).all()
    plant_list = convert_plant_results(results)
    return plant_list


# %%


