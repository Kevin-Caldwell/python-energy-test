import osmnx.features as featurelib
import geopandas
import matplotlib.pyplot as plt

def download_map_features(query, tags) -> geopandas.GeoDataFrame:
    """Wrapper function for downloading Map Features."""
    return featurelib.features_from_place(
        query=query, 
        tags=tags
        )

def latlong_to_xy(lat, long):
    """Convert Lattitude and Longitude Data to approximate distances in meters"""
    return (lat * 11100, long * 87870)

def extract_feature_geometry(features: geopandas.GeoDataFrame):
    """Extracts Geometry from a GeoDataFrame. Must have a 
    .iloc.geometry.exterior.coords.xy Property"""
    geometry = []

    for building in features.iloc:

        if building.geometry.geom_type == 'Polygon':
            x, y = building.geometry.exterior.coords.xy

            x = x.tolist()
            y = y.tolist()

            geometry.append([x, y])
    return geometry

def plot_polygon_set(polygon_set):
    """Plots a list of polygons. The polygons are described as a list of lists.
    The first list contains all the x-values involved, and the second contains
    all the corresponding y-coordinates."""
    
    for polygon in polygon_set:
        for i in range(len(polygon[0])):
            plt.plot(polygon[0], polygon[1])

    plt.show()


place_name = "University of Toronto"
feature_tags = {"building": True}

if __name__ == "__main__":
    print("Downloading Feature Data...")
    features: geopandas.GeoDataFrame = download_map_features(
        query=place_name, 
        tags=feature_tags
    )
    print("Feature Data Downloaded!")
    print("Compiling Building Data...")
    buildings = extract_feature_geometry(features)
    print("Plotting Building Contours...")
    plot_polygon_set(buildings)