from fastapi import APIRouter
import pandas as pd
import wbgapi as wb

router = APIRouter()

# PART 3. GET CEREAL YIELD

countries = ['AFG','ARE','ARG','ARM','AUS','AUT','AZE','BEL','BEN','BGD','ZWE', 'ZMB', 'YEM', 'PSE']

@router.get("/yield")
async def get_cereal_yield_all():

    """
    Objective - Returns a list of available information years for that country
    1. Requisite - If no year is provided, returns list of available years.
    2. Requisite - If data for the country is not found, returns an empty response
    """
    df = wb.data.DataFrame('AG.PRD.CREL.MT', countries )
    df = df.dropna(how='all', axis=1)
    df = df.dropna(how='all', axis=0)
 
    return df.to_json()

@router.get("/yield/{country}")
async def get_cereal_yield(country):
    """
    Objective - Returns a list of available information years for that country
    1. Requisite - If no year is provided, returns list of available years.
    2. Requisite - If data for the country is not found, returns an empty response
    """
    try:
        df = wb.data.DataFrame('AG.YLD.CREL.KG', [str(country)] )
        df = df.dropna(how='all', axis=1)
        return [column[2:] for column in df.columns]
    except:
        return ""


@router.get("/yield/{country}/{year}")
async def get_cereal_yield(country, year:int):

    """
    Objective - Returns the cereal yield of a country for a given year (in kg/Ha, as an
    integer. 
    1. Requisite - If no year is provided, returns list of available years.
    """
    try:
        df = wb.data.DataFrame('AG.YLD.CREL.KG', [str(country)], time=int(year))
        cereal_yield = df.values[0]
        if pd.isnull(cereal_yield):
            return "" # Response if year exist in the dataframe but this country don't have record.
        else:
            return float(cereal_yield) # Response if everything correct.
    except: 
        return "" # Response if the year directly don't exist in the DB


# PART 4. GET CEREAL LAND

@router.get("/land/{country}")
async def get_cereal_land(country):
    """
    Objective - Returns a list of available information years for that country
    1. Requisite - If no year is provided, returns list of available years.
    2. Requisite - If data for the country is not found, returns an empty response
    """
    try:
        df = wb.data.DataFrame('AG.LND.CREL.HA', [str(country)])
        df = df.dropna(how='all', axis=1)
        return [column[2:] for column in df.columns]
    except:
        return ""


@router.get("/land/{country}/{year}")
async def get_cereal_land(country, year:int):

    """
    Objective - Returns the surface of a country dedicated to cereal production, for a
    given year (in hectares)
    1. Requisite - If no year is provided, returns list of available years.
    """
    try:
        df = wb.data.DataFrame('AG.LND.CREL.HA', [str(country)], time=int(year))
        cereal_land = df.values[0]
        if pd.isnull(cereal_land):
            return "" # Response if year exist in the dataframe but this country don't have record.
        else:
            return float(cereal_land) # Response if everything correct.
    except: 
        return "" # Response if the year directly don't exist in the DB