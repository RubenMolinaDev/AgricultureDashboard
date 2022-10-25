from fastapi import APIRouter
import json
import pandas as pd
from urllib.request import urlopen
import wbgapi as wb

router = APIRouter()

@router.get("/all_id", status_code=200)
def get_countries_id():

    """
    Returns all the countries id independently of the region, as a list
    This is not an API endpoint, is a helper function.
    """

    URL = 'http://api.worldbank.org/v2/country?per_page=99999&format=json'
 
    # store the response of URL
    response = urlopen(URL)
    data_json = json.loads(response.read())
    all_info = pd.json_normalize(data_json[1])[["id", "name", "region.id", 'capitalCity']] # In this point we have a Pandas dataset of name and region.
    all_info = all_info[(all_info['capitalCity'] != "")]
    countries = all_info["id"].to_list()

    return countries
    
@router.get("/all_name")
def get_countries_name():

    """
    Returns all the countries id independently of the region, as a list
    This is not an API endpoint, is a helper function.
    """

    URL = 'http://api.worldbank.org/v2/country?per_page=99999&format=json'
 
    # store the response of URL
    response = urlopen(URL)
    data_json = json.loads(response.read())
    all_info = pd.json_normalize(data_json[1])[["id", "name", "region.id", 'capitalCity']] # In this point we have a Pandas dataset of name and region.
    all_info = all_info[(all_info['capitalCity'] != "")]
    countries = all_info["name"].to_list()

    return countries

@router.get("/{region}")
def get_countries(region):

    """
    Returns all the countries in a given region, as a list
    """

    URL = 'http://api.worldbank.org/v2/country?per_page=99999&format=json'
 
    # store the response of URL
    response = urlopen(URL)
    data_json = json.loads(response.read())
    all_info = pd.json_normalize(data_json[1])[["id", "name", "region.id", 'capitalCity']] # In this point we have a Pandas dataset of name and region.
    all_info = all_info[(all_info['capitalCity'] != "")]
    all_info = all_info[all_info['region.id'] == region]
    countries = all_info["id"].to_list()

    return countries