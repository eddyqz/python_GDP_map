# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:10:28 2020

@author: eddyz

GDP_Render_to_Map

Reads in worldwide GDP data from a CSV file, then displays the 
varying levels of GDP for a given year on a world map.
Note: the numbers on the map are not actual GDP; they are log(GDP) in order
to even out the shading on the map.
The GDP map is written to a file and rendered in a browser.

This program depends on a gdpinfo dictionary, passed as an argument
when running the program, to accurately read data from the CSV file.
The gdpinfo dictionary can be manually adjusted by the user according
to the GDP data table, thus allowing this program to work for any GDP table. 
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - The name of the column that contains all the headers for the 
				  rows, typically the first column
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of OrderedDicts where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner OrderedDicts contain tuples that contain column names and
      field values for that row.
    """
    table = {}
    with open(filename, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries. The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    code_name_dict = {}
    not_found_set = set()
	
    for code in plot_countries:
        if plot_countries[code] in gdp_countries:
            code_name_dict[code] = plot_countries[code]
        else:
            not_found_set.add(code)
	
    return_tuple = (code_name_dict, not_found_set)
    return return_tuple


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
	
    data = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
	# data is a table of gdp data in nested dict/OrderedDict form
    
    data_nested_dict = {} 
	# dict of OrderedDicts converted to nested dict
    for key, value in data.items():
        data_nested_dict[key] = dict(value)
	
    code_tuple = reconcile_countries_by_name(plot_countries, data_nested_dict)
	# generates dictionary of countries in gdp data file that can be plotted by pygal
	
    log_gdp_dict = {} # dict that maps country codes to log of gdp value, to be returned at the end
    not_found_set = code_tuple[1] # set of countries not found in the gdp data file
    no_data_set = set() # set of countries with no data in gdp data file
    
    for code, country_name in code_tuple[0].items(): 
        if data_nested_dict[country_name][year] != "": # if field isn't empty, i.e. there is data 
            log_gdp_dict[code] = math.log10(float(data_nested_dict[country_name][year])) 
        else: 
            no_data_set.add(code) 

    return (log_gdp_dict, not_found_set, no_data_set)


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
	
    map_tuple = build_map_dict_by_name(gdpinfo, plot_countries, year) 
	# tuple containing log_gdp_dict, not_found_set, and no_data_set
	
    gdp_world_map = pygal.maps.world.World(show_legend = False, human_readable = True, fill = True) 
	# initializes the map plot with some attributes
	
    gdp_world_map.title = "GDP by Country in {0}".format(year)
	
    gdp_world_map.add("In {0}".format(year), map_tuple[0]) 
	# adds the log_gdp_dict to the map plot
	
    gdp_world_map.render_to_file(map_file)
    gdp_world_map.render_in_browser()
	


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "gdp_table.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2019,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "World_GDP_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "World_GDP_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "World_GDP_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "World_GDP_2010.svg")


# test_render_world_map()

