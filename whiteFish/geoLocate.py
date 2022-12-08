import csv
import threading
import time

import geopandas as gpd
import osmnx as ox
import networkx as nx
import folium

from whiteFish.models import FireStation, Home


def geocode_address(address, crs=4326):
    time.sleep(0.5)
    geocode = gpd.tools.geocode(address, provider='nominatim', user_agent="whiteFish").to_crs(crs)
    if geocode.iloc[0].geometry.geom_type != 'Point':
        geocode = gpd.tools.geocode(address, provider='googlev3',
                                    api_key='AIzaSyDw_Vqyee1jpHFC8uwtFg8fAySzMC6K86A',
                                    user_agent="whiteFish").to_crs(crs)
    return geocode.iloc[0].geometry.y, geocode.iloc[0].geometry.x


def get_shortest_distance(G, origin_point, destination_point):
    if origin_point is None or destination_point is None:
        return 0

    orig_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
    destination_node = ox.distance.nearest_nodes(G,
                                                 destination_point[1], destination_point[0])

    route = nx.shortest_path(G, orig_node, destination_node, weight='length')

    edge_lengths = ox.utils_graph.get_route_edge_attributes(
        G, route, 'length')
    total_route_length = sum(edge_lengths)
    return total_route_length / 1609


def visualize_graph(path):
    print('visualizing graph')
    m = folium.Map(location=[48.4456, -114.3771], zoom_start=12)
    for fire_station in FireStation.objects.all():
        folium.Marker(location=[fire_station.cords_lat, fire_station.cords_long],
                      popup=fire_station.address, icon=folium.Icon(color='red')).add_to(m)

    for home in Home.objects.all():
        folium.Marker(location=[home.cords_lat, home.cords_long],
                      popup=home.property_location.replace("`", ""), icon=folium.Icon(color='blue')).add_to(m)

    m.save(path)
    print('graph saved')

# if __name__ == '__main__':
#     # get a graph
#     ox.config(use_cache=True)
#     # with open("fire_station_locations", "r") as f:
#     #     fire_stations = f.read().splitlines()
#     #
#     # with open("home_addresses", "r") as f:
#     #     home_addresses = f.read().splitlines()
#
#     # fire_stations_cords = []
#     # for fire_station in fire_stations:
#     #     try:
#     #         fire_stations_cords.append(geocode_address(fire_station))
#     #     except:
#     #         fire_stations_cords.append(None)
#     #
#     # with open("fire_station_locations_cords.csv", "w") as f:
#     #     writer = csv.writer(f)
#     #     writer.writerows(fire_stations_cords)
#     #
#     # print("Fire stations cords written to file")
#     # home_addresses_cords = []
#     # home_addresses = [x+", Whitefish, MT 59937" for x in home_addresses]
#     # for home_address in home_addresses:
#     #     try:
#     #         home_addresses_cords.append(geocode_address(home_address))
#     #     except:
#     #         home_addresses_cords.append(None)
#     #
#     # with open("home_addresses_cords.csv", "w") as f:
#     #     writer = csv.writer(f)
#     #     writer.writerows(home_addresses_cords)
#     #
#     # print("Home addresses cords written to file")
#     #
#     G = ox.graph_from_place('Flathead County, Montana, USA', network_type='drive')
#
#     with open ("fire_station_locations_cords.csv", "r") as f:
#         reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
#         fire_stations_cords = list(reader)
#
#     with open("home_addresses_cords.csv", "r") as f:
#         reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
#         home_addresses_cords = list(reader)
#     n = len(home_addresses_cords)
#     m = len(fire_stations_cords)
#     distances = [[0 for i in range(m)] for j in range(n)]
#
#     count = 0
#     for i in range(n):
#         for j in range(m):
#             distances[i][j] = get_shortest_distance(G, home_addresses_cords[i], fire_stations_cords[j])
#             count += 1
#             print(count)
#
#     with open("out.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(distances)
#
#     # G = ox.graph_from_place('Flathead County, Montana, USA', network_type='drive')
#     # origin = geocode_address("1345 HODGSON RD, Whitefish, MT 59937")
#     # destination = geocode_address("4686 US Highway 93 West, Whitefish, MT 59937")
#     #
#     # print(get_shortest_distance(G, origin, destination))
