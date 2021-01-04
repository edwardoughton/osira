"""
Process settlement layer

Written by Ed Oughton.

December 2020

"""
import os
import configparser
import geopandas as gpd

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


def load_mastermap(path):
    """
    This function loads OS MasterMap functional site data.

    Parameters
    ----------
    path : string
        Path to the .shp file to be read.

    """
    sites = gpd.read_file(path, crs='epsg:27700')
    sites = sites[['geometry', 'functionth', 'function', 'distinctiv']]

    functions = ['Utility or Industrial', 'Rail Transport', 'Air Transport']
    sites = sites[sites['functionth'].isin(functions)]

    path_out = os.path.join(DATA_INTERMEDIATE, 'all_sites.shp')
    sites.to_file(path_out, crs='epsg:27700')


def process_elec_distribution_sites():
    """
    Obtain electricity distribution sites.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'all_sites.shp')
    sites = gpd.read_file(path, crs='epsg:27700')

    polys = sites.loc[sites['function'] == 'Electricity Distribution']
    points = polys.copy()
    points['geometry'] = points['geometry'].centroid

    path_out = os.path.join(DATA_INTERMEDIATE, 'elec_distribution.shp')
    points.to_file(path_out, crs='epsg:27700')


def process_gas_sites():
    """
    Obtain gas distribution or storage sites.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'all_sites.shp')
    sites = gpd.read_file(path, crs='epsg:27700')

    polys = sites.loc[sites['function'] == 'Gas Distribution or Storage']
    points = polys.copy()
    points['geometry'] = points['geometry'].centroid

    path_out = os.path.join(DATA_INTERMEDIATE, 'gas_sites.shp')
    points.to_file(path_out, crs='epsg:27700')


def process_railway_stations():
    """
    Obtain railway station sites.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'all_sites.shp')
    sites = gpd.read_file(path, crs='epsg:27700')

    polys = sites.loc[sites['function'] == 'Railway Station']
    points = polys.copy()
    points['geometry'] = points['geometry'].centroid

    path_out = os.path.join(DATA_INTERMEDIATE, 'railway_stations.shp')
    points.to_file(path_out, crs='epsg:27700')


def process_airports():
    """
    Obtain airport sites.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'all_sites.shp')
    sites = gpd.read_file(path, crs='epsg:27700')

    polys = sites.loc[sites['functionth'] == 'Air Transport']
    polys = polys[polys['distinctiv'].str.contains('Airport', na=False)]

    points = polys.copy()
    points['geometry'] = points['geometry'].centroid

    path_out = os.path.join(DATA_INTERMEDIATE, 'airports.shp')
    points.to_file(path_out, crs='epsg:27700')


if __name__ == '__main__':

    path = os.path.join(DATA_RAW, 'mastermap', 'Functional_Site.shp')
    load_mastermap(path)

    process_elec_distribution_sites()

    process_gas_sites()

    process_railway_stations()

    process_airports()
