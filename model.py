# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 15:06:17 2022

@author: keatin6
"""


# %% IMPORT NEEDED LIBRARIES

from sqlalchemy import Column, create_engine
from sqlalchemy import Integer, ForeignKey, String, Date
from sqlalchemy.ext.declarative import declarative_base

# %% SETUP THE DATABASE ENGINE

engine = create_engine("sqlite:///PlantingGuideDB.db", echo=True)
Base = declarative_base()
metadata = Base.metadata

# %% 

class OlvPlant:
    def __init__(self, category, subcategory, plant_type, plant, scientific):
        self.category = category
        self.subcategory = subcategory
        self.plant_type = plant_type
        self.plant = plant
        self.scientific = scientific

# %% SETUP THE DATABASE ENGINE

class upg_Zone(Base):
    __tablename__ = "upg_Zones"
    
    ZoneID = Column(Integer, primary_key=True)
    LFD_min = Column("LFD_min", Date)
    LFD_max = Column("LFD_max", Date)
    FFD_min = Column("FFD_min", Date)
    FFD_max = Column("FFD_max", Date)
    

# %% 
    
class upg_ZipCode(Base):
    __tablename__ = "upg_ZipCodes"
    
    ZipCode = Column(String, primary_key=True)
    Municipality = Column("Municipality",String)
    County  = Column("County", String)
    StateCode = Column("StateCode", String)
    ZoneID = Column("ZoneID", Integer, ForeignKey("upg_Zones.ZoneID"))
    ZoneCode = Column("ZoneCode", String)


# %% 

class upg_Category(Base):
    __tablename__ = "upg_Categories"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("Category", String)
    

# %% 
    
class upg_Subcategory(Base):
    __tablename__ = "upg_Subcategories"
    
    ID = Column(Integer, primary_key=True)
    PlantTypeID = Column("PlantTypeID", Integer, 
                         ForeignKey("upg_PlantTypes.PlantTypeID"))
    Name = Column("Subcategory", String)
    Rank = Column("Rank", Integer)


# %% 

class upg_LightType(Base):
    __tablename__ = "upg_LightTypes"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("LightType", String)
    

# %% 
    
class upg_Season(Base):
    __tablename__ = "upg_Seasons"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("Season", String)
    

# %% 

class upg_Soil(Base):
    __tablename__ = "upg_Soils"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("SoilName", String)
    Description = Column("SoilDescription", String)


# %% 

class upg_LifeSpan(Base):
    __tablename__ = "upg_LifeSpans"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("LifeSpan", String)


# %% 

class upg_WateringType(Base):
    __tablename__ = "upg_WateringTypes"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("WateringType", String)


# %% 

class upg_HardinessType(Base):
    __tablename__ = "upg_HardinessTypes"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("HardinessType", String)
    Description = Column("HardinessDesc", String)


# %% 

class upg_PlantingMethod(Base):
    __tablename__ = "upg_PlantingMethods"
    
    ID = Column(Integer, primary_key=True)
    Name = Column("PlantingMethod", String)


# %% 

class upg_Bionomic(Base):
   __tablename__ = "upg_Taxonomy" 
   
   ScientificID = Column(Integer, primary_key=True)
   Genus = Column("Genus", String)
   Species = Column("Species", String)

# %% 

class upg_PlantType(Base):
    __tablename__ = "upg_PlantTypes"
    
    ID = Column("PlantTypeID",Integer, primary_key=True)
    CategoryID = Column("CategoryID", Integer, ForeignKey("upg_Categories.ID"))
    PlantCode = Column("PlantCode", String)
    Name = Column("PlantType", String)
    PlantTypeDesc = Column("PlantTypeDesc", String)
    LightTypeID =  Column("LightTypeID", Integer, 
                          ForeignKey("upg_LightTypes.ID"))
    SoilID = Column("SoilID", Integer, ForeignKey("upg_Soils.ID"))
    LifeSpanID = Column("LifeSpanID", Integer, ForeignKey("upg_LifeSpans.ID"))
    WateringTypeID = Column("WateringTypeID", Integer, 
                            ForeignKey("upg_WateringTypes.ID"))
    HardinessTypeID = Column("HardinessID", Integer, 
                             ForeignKey("upg_HardinessTypes.ID"))
    SeasonID = Column("SeasonID", Integer, ForeignKey("upg_Seasons.ID"))
    MethodID = Column("MethodID", Integer, 
                      ForeignKey("upg_PlantingMethods.ID"))


# %% 

class upg_Plant(Base):
    __tablename__ = "upg_Plants"
    
    PlantID = Column(Integer, primary_key=True)
    PlantTypeID = Column("PlantTypeID", Integer, 
                         ForeignKey("upg_PlantTypes.PlantTypeID"))
    ScientificID = Column("ScientificID", Integer, 
                          ForeignKey("upg_Taxonomy.ScientificID"))
    PlantName = Column("PlantName", String)
    PlantDesc = Column("PlantDesc", String) 
    SubcategoryID = Column("SubcategoryID", Integer, 
                           ForeignKey("upg_Subcategories.ID"))
    PlantingDepth = Column("PlantingDepth", Integer)
    DTG_min = Column("DTG_min", Integer)
    DTG_max = Column("DTG_max", Integer)
    DTM_min = Column("DTM_min", Integer)
    DTM_max  = Column("DTM_max", Integer)
    Height_min = Column("Height_min", Integer)
    Height_max = Column("Height_max", Integer)
    Size_min = Column("Size_min", Integer)
    Size_max = Column("Size_max", Integer)
    SourceID = Column("SourceID", Integer, ForeignKey("upg_Sources.SourceID"))
    Zones = Column("Zones", String)
    
    
# %% 

class upg_Source(Base):
    __tablename__ = "upg_Sources"
    
    SourceID = Column(Integer, primary_key=True)
    SourceName = Column("SourceName", String)
    
# %% SETUP THE DATABASE ENGINE

Base.metadata.create_all(engine)

# %% 