"""
Process settlement layer

Written by Ed Oughton.

December 2020

"""
import os
import configparser
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, box
from shapely.ops import nearest_points

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

    points['id'] = (
        points['geometry'].apply(lambda p: str(p.x)) +
        '_' +
        points['geometry'].apply(lambda p: str(p.y))
    )

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


def connect_assets_to_elec_nodes():
    """
    Affiliate local assets with their nearest electricity node.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'elec_distribution.shp')
    elec_sites = gpd.read_file(path)

    path = os.path.join(DATA_INTERMEDIATE, 'gas_sites.shp')
    gas_sites = gpd.read_file(path)

    path = os.path.join(DATA_INTERMEDIATE, 'airports.shp')
    airports = gpd.read_file(path)

    path = os.path.join(DATA_INTERMEDIATE, 'railway_stations.shp')
    railway_stations = gpd.read_file(path)

    sites = gas_sites.append(airports)
    sites = sites.append(railway_stations)

    output_edges = []
    output_nodes = []

    for idx, site in sites.iterrows():

        nearest = nearest_points(site['geometry'], elec_sites.unary_union)[1]

        geom = LineString([
                    (
                        site['geometry'].coords[0][0],
                        site['geometry'].coords[0][1]
                    ),
                    (
                        nearest.coords[0][0],
                        nearest.coords[0][1]
                    ),
                ])

        nearest = gpd.GeoDataFrame({'geometry': [nearest]}, index=[idx], crs='epsg:27700')
        nearest['geometry'] = nearest['geometry'].buffer(10)

        elec_site = gpd.overlay(elec_sites, nearest, how='intersection')

        output_edges.append({
            'geometry': geom,
            'properties': {
                'origin_elec': elec_site['id'][0],
                'dest_funcionth': site['functionth'],
                'dest_funcion': site['function'],
                'dest_distinctiv': site['distinctiv'],
            },
        })

        output_nodes.append({
            'geometry': site['geometry'],
            'properties': {
                'origin_elec': elec_site['id'][0],
                'dest_funcionth': site['functionth'],
                'dest_funcion': site['function'],
                'dest_distinctiv': site['distinctiv'],
            },
        })

    output_edges = gpd.GeoDataFrame.from_features(output_edges, crs='epsg:27700')
    path = os.path.join(DATA_INTERMEDIATE, 'network_edges.shp')
    output_edges.to_file(path, crs='epsg:27700')

    output_nodes = gpd.GeoDataFrame.from_features(output_nodes, crs='epsg:27700')
    path = os.path.join(DATA_INTERMEDIATE, 'network_nodes.shp')
    output_nodes.to_file(path, crs='epsg:27700')


def process_lsoa_boundaries(path):
    """
    This function loads England and Wales Lower Layer Super Output Area boundaries.

    Parameters
    ----------
    path : string
        Path to the .shp file to be read.

    """
    boundaries = gpd.read_file(path, crs='epsg:27700')

    path = os.path.join(DATA_INTERMEDIATE, 'all_sites.shp')
    all_sites = gpd.read_file(path, crs='epsg:27700')
    bbox = box(*all_sites.total_bounds)
    bbox = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs='epsg:27700')

    boundaries = gpd.overlay(boundaries, bbox, how='intersection')

    path_out = os.path.join(DATA_INTERMEDIATE, 'oa_boundaries.shp')
    boundaries.to_file(path_out, crs='epsg:27700')

    boundaries['geometry'] = boundaries['geometry'].centroid
    path_out = os.path.join(DATA_INTERMEDIATE, 'oa_centroids.shp')
    boundaries.to_file(path_out, crs='epsg:27700')


def add_population_to_lsoa_centroid(path):
    """
    This function adds population estimates to LSOA centroids.

    Parameters
    ----------
    path : string
        Path to the .csv population file to be read.

    """
    pop_data = pd.read_csv(path)

    path = os.path.join(DATA_INTERMEDIATE, 'oa_centroids.shp')
    output_areas = gpd.read_file(path, crs='epsg:27700')

    output_areas = output_areas.merge(pop_data, left_on='LSOA11CD', right_on='code')

    path_out = os.path.join(DATA_INTERMEDIATE, 'oa_centroids.shp')
    output_areas.to_file(path_out, crs='epsg:27700')


def estimate_pop_per_node():
    """
    This function estimates the population served by each elec distribution node.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'elec_distribution.shp')
    elec_sites = gpd.read_file(path)

    path = os.path.join(DATA_INTERMEDIATE, 'oa_centroids.shp')
    output_areas = gpd.read_file(path, crs='epsg:27700')

    output_centroids = []

    for idx, output_area in output_areas.iterrows():

        nearest = nearest_points(output_area['geometry'], elec_sites.unary_union)[1]

        output_centroids.append({
            'geometry': output_area['geometry'],
            'properties': {
                'origin_elec': str(nearest.coords.xy[0][0]) +
                    '_' +
                    str(nearest.coords.xy[1][0]),
                'population': output_area['population'],
            },
        })

    output_centroids = gpd.GeoDataFrame.from_features(output_centroids, crs='epsg:27700')
    path_out = os.path.join(DATA_INTERMEDIATE, 'oa_centroids.shp')
    output_centroids.to_file(path_out, crs='epsg:27700')

    unique_nodes = set()

    for idx, output_area in output_centroids.iterrows():
        unique_nodes.add(output_area['origin_elec'])

    pop_per_node = []

    for node_id in list(unique_nodes):

        population = 0

        for idx, output_area in output_centroids.iterrows():
            if output_area['origin_elec'] == node_id:
                population += output_area['population']

        pop_per_node.append({
            'id': node_id,
            'population': population,
        })

    pop_per_node = pd.DataFrame(pop_per_node)

    path_out = os.path.join(DATA_INTERMEDIATE, 'pop_by_elec_node.csv')
    pop_per_node.to_csv(path_out, index=False)


def add_pop_to_nodes():
    """
    This function adds the population to each elec distribution node.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'pop_by_elec_node.csv')
    pop_data = pd.read_csv(path)

    path = os.path.join(DATA_INTERMEDIATE, 'elec_distribution.shp')
    elec_nodes = gpd.read_file(path, crs='epsg:27700')

    output = []

    for idx, item in pop_data.iterrows():
        for idx, elec_node in elec_nodes.iterrows():
            if item['id'] == elec_node['id']:
                output.append({
                    'geometry': elec_node['geometry'],
                    'properties': {
                        'id': elec_node['id'],
                        'population': item['population'],
                    },
                })

    output = gpd.GeoDataFrame.from_features(output)

    path = os.path.join(DATA_INTERMEDIATE, 'elec_distribution.shp')
    output.to_file(path, crs='epsg:27700')


if __name__ == '__main__':

    print('Loading MasterMap data')
    path = os.path.join(DATA_RAW, 'mastermap', 'Functional_Site.shp')
    load_mastermap(path)

    print('Processing electricity sites')
    process_elec_distribution_sites()

    print('Processing gas sites')
    process_gas_sites()

    print('Processing railway sites')
    process_railway_stations()

    print('Processing airports')
    process_airports()

    print('Connecting assets to electricity nodes')
    connect_assets_to_elec_nodes()

    print('Processing LSOA boundaries')
    filename = 'Lower_Layer_Super_Output_Areas__December_2011__Boundaries_EW_BFC.shp'
    path = os.path.join(DATA_RAW, 'OAs', filename)
    process_lsoa_boundaries(path)

    print('Adding population to LSOA centroids')
    path = os.path.join(DATA_RAW, 'pop_by_OA', '8247583.csv')
    add_population_to_lsoa_centroid(path)

    print('Estimating the population per node')
    estimate_pop_per_node()

    print('Adding the population to electricity nodes')
    add_pop_to_nodes()
