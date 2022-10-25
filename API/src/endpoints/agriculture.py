from fastapi import APIRouter
import pandas as pd
import wbgapi as wb

router = APIRouter()

# This page contains the endpoints related to the agricultural land.

countries = ['AFG','ARE','ARG','ARM','AUS','AUT','AZE','BEL','BEN','BGD','ZWE', 'ZMB', 'YEM', 'PSE']

@router.get("/surface")
async def get_agro_land_srfc_all():

    """
    Returns a dataframe for all the countries with information
    about the quantity of Agricultural land in sq.km
    """
    df = wb.data.DataFrame('AG.LND.AGRI.K2', countries )
    df = df.dropna(how='all', axis=1)
    df = df.dropna(how='all', axis=0)

    return df.to_json()

@router.get("/surface/{country}")
async def get_agro_land_srfc(country):

    """
    Returns a list of available information years for that country.
    If data for the country is not found, returns an empty response
    """
    try:
        df = wb.data.DataFrame('AG.LND.AGRI.K2', countries )
        df = df.dropna(how='all', axis=1)
        return [column[2:] for column in df.columns]
    except:
        return ""

@router.get("/surface/{country}/{year}")
async def get_agro_land_srfc(country, year):

    """
    Returns a country's agricultural land surface (in sq. km) for a given
    year, as a float. If no year is provided, returns list of available years.
    """
    try:
        df = wb.data.DataFrame('AG.LND.AGRI.K2', [str(country)], time=int(year))
        agr_surface = df.values[0]
        if pd.isnull(agr_surface):
            return "" # Response if year exist in the dataframe but this country don't have record.
        else:
            return float(agr_surface) # Response if everything correct.
    except: 
        return "" # Response if the year directly don't exist in the DB


@router.get("/surface_percentage")
async def get_pct_agro_surface():

    """
    Returns a dataframe for all the countries with the percentage 
    of agricultural land regarding the country.
    """

    df = wb.data.DataFrame('AG.LND.AGRI.ZS', countries  )
    df = df.dropna(how='all', axis=1)
    df = df.dropna(how='all', axis=0)

    return df.to_json()


@router.get("/surface_irrigation")
async def get_pct_irr_agro_surface():

    """
    Returns a dataframe for all the countries with the percentage 
    of irrigated agricultural land.
    """

    df = wb.data.DataFrame('AG.LND.IRIG.AG.ZS', countries  )
    df = df.dropna(how='all', axis=1)
    df = df.dropna(how='all', axis=0)

    return df.to_json()