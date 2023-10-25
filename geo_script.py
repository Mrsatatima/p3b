from qgis.core import(QgsFeature, QgsVectorLayer,QgsFeatureRequest,QgsFields,QgsApplication )
from processing.core.Processing import Processing
import processing
import random

from helper import *

path = "C:/Users/ASUS/AppData/Local/Temp/tmp4d4rmkcc.py"
QgsApplication.setPrefixPath(path, True)
qgs = QgsApplication([], False)

qgs.initQgis()
Processing.initialize()


def crt_subset_lyr(layer, query):
    """
        Creates a subset of a layer by pyqgis processing 
        selection by expression,
        Input:
            layer: The layer you want to get subset from (QgsVectorLayer)
            query: Expression to be ised for querying (str)
        Ouput:
            memory_layer: subset of the layer (QgsVectorLayer)

    """
    # Create a memory layer
    set_extent_uri = f"polygon?crs={layer.crs().authid()}"
    memory_layer = QgsVectorLayer(set_extent_uri, "set_extent", "memory")
    memory_layer.startEditing()
    # Set the memory layer's fields
    memory_layer.dataProvider().addAttributes(layer.dataProvider().fields().toList())
    memory_layer.updateFields()

    parameters = {'INPUT': layer,
                  'EXPRESSION': query,
                  'METHOD': 0,
                  }
    run_selection = processing.run('qgis:selectbyexpression', parameters)
    # Add the selected features to the memory layer
    selected = run_selection['OUTPUT'].selectedFeatures()
    outFeat = QgsFeature()
    for feature in selected:
        outFeat.setGeometry(feature.geometry())
        outFeat.setAttributes(feature.attributes())
        memory_layer.dataProvider().addFeatures([outFeat])
        memory_layer.updateExtents()
    memory_layer.commitChanges()
    return memory_layer


def clip_set_ext_layer(layer, clip_layer):
    """
        this function clips features that are within another layer
        it uses the pyqgis processing clip
        Input:
            layer: The layer whose features needs to be clip (QgsVectorLayer)
            clip_layer: layer for to be used for cliping (QgsVectorLayer)
        Output:
            clipped_layer: Clipped features (QgsVectorLayer)
    """
    parameters = {'INPUT': layer,
                  'OVERLAY': clip_layer,
                  'OUTPUT': 'TEMPORARY_OUTPUT',
                  }
    clipped_layer = processing.run('native:clip', parameters)
    return clipped_layer["OUTPUT"]


def create_random_point(layer):
    """
        chooses the extent with the largest bld_count
        an create a random point within the extent
        Input:
            layer: Extents layers to choose largest from (QgsVectoLayer)
        Output:
        Point: The x and y coordinate of the point (tuple) 
    """
    layer = layer.getFeatures()
    extents = [extent for extent in layer if extent["bld_count"] != "1-50"]
    dct = {}
    for idx, extent in enumerate(extents):
        if extent["bld_count"] == "51-100":
            dct[str(idx)] = 1
        elif extent["bld_count"] == "51-100":
            dct[str(idx)] = 2
        else:
            dct[str(idx)] = 3
    extent = extents[int(max(dct.values()))]
    geom = extent.geometry() 
    random_x = random.uniform(geom.boundingBox().xMinimum(), geom.boundingBox().xMaximum())
    random_y = random.uniform(geom.boundingBox().yMinimum(), geom.boundingBox().yMaximum())
    point = (random_x, random_y)
    return point


def geo_location(wards_layer, extent, state, lga, ward):
    """
        takes a ward and create a random point within the ward
        Input:
            wards_layer: GRID3 Nigeria wards layer (QgsVectorLayer)
            extent: GRID3 Nigeria settlemetn extents layer (QgsVectorLayer)
        Output:
            location: x and y coordinates of the location (tuple)
    """
    wards_layer = QgsVectorLayer(wards_layer, "wards", "ogr")
    extent = QgsVectorLayer(extent, "set_extent", "ogr")
    query = f'"statename"  =  \'{state}\' AND  "lganame"  =  \'{kwara_lga_map[lga]}\'AND "wardname" = \'{kwara_wards_map[ward]}\''
    ward_layer = crt_subset_lyr(wards_layer, query)
    ward_extent = clip_set_ext_layer(extent, ward_layer)
    location = create_random_point(ward_extent)
    return location
