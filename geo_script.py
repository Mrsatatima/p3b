from qgis.core import(QgsFeature, QgsVectorLayer,QgsFeatureRequest,QgsFields,QgsApplication,QgsGeometry )
from processing.core.Processing import Processing
import processing
import random
from processing.tools import dataobjects

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
    context = dataobjects.createContext()
    context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)
    clipped_layer = processing.run('native:clip', parameters, context=context)

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
    extent_layer = layer.getFeatures()
    extents = [extent for extent in extent_layer]
    dct = {}
    for idx, extent in enumerate(extents):
        if extent["bld_count"] == "1-50" and 1 not in dct.values():
            dct[str(idx)] = 0
        elif extent["bld_count"] == "51-100" and 1 not in dct.values():
            dct[str(idx)] = 1
        elif extent["bld_count"] == "101-250" and 2 not in dct.values():
            dct[str(idx)] = 2
        elif extent["bld_count"] == "251-1000" and 3 not in dct.values():
            dct[str(idx)] = 3
        elif extent["bld_count"] == "1001 and up" and 4 not in dct.values():
            dct[str(idx)] = 4
        else:
            continue
    extent = extents[int(max(dct, key=dct.get))]
    extent_center = extent.geometry().centroid().asPoint()
    x = extent_center.x()
    y = extent_center.y()
    point = (x, y)
    return point


def geo_location(wards_layer, extent, state, lga, ward, lga_dct, ward_dct):
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
    # print(ward_dct[ward.strip().lower()])
    query = f'"statename"  =  \'{state}\' AND  "lganame"  =  \'{lga_dct[lga.strip().lower()].title()}\'AND "wardname" = \'{ward_dct[lga.strip().lower()][ward.strip().lower()].title()}\''
    ward_layer = crt_subset_lyr(wards_layer, query)
    if list(ward_layer.getFeatures())[0]['status'] == "Invalid":
        return ("x",'y')
    ward_extent = clip_set_ext_layer(extent, ward_layer)
    location = create_random_point(ward_extent)
    return location
