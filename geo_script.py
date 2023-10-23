from qgis.core import(QgsFeature, QgsVectorLayer,QgsFeatureRequest,QgsFields,QgsApplication )
from processing.core.Processing import Processing
import processing

from helper import *

path ="C:/Users/ASUS/AppData/Local/Temp/tmp4d4rmkcc.py"
QgsApplication.setPrefixPath(path, True)
qgs = QgsApplication([], False)

qgs.initQgis()
Processing.initialize()



def crt_subset_lyr(layer,query):
    selected = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    # Create a memory layer
    set_extent_uri = f"polygon?crs={layer.crs().authid()}"
    memory_layer = QgsVectorLayer(set_extent_uri, "set_extent", "memory")
    memory_layer.startEditing()
    # Set the memory layer's fields
    memory_layer.dataProvider().addAttributes(layer.dataProvider().fields().toList())
    memory_layer.updateFields()

    # Add the selected features to the memory layer
    outFeat = QgsFeature()
    for feature in selected:
        outFeat.setGeometry(feature.geometry())
        outFeat.setAttributes(feature.attributes())
        memory_layer.dataProvider().addFeatures([outFeat])
        memory_layer.updateExtents()
    memory_layer.commitChanges()

    return memory_layer


def clip_set_ext_layer(layer, clip_layer):
    set_extent_uri = f"polygon?crs={layer.crs().authid()}"
    set_extent_layer = QgsVectorLayer(set_extent_uri, "set_extent", "memory")
    set_extent_layer_data = set_extent_layer.dataProvider()
    set_extent_layer.startEditing()
    set_extent_layer_fields = QgsFields(layer.fields())
    set_extent_layer_data.addAttributes(set_extent_layer_fields)
    set_extent_layer.updateFields()

    parameters = { 'INPUT' : layer,
               'INTERSECT' : clip_layer, 
               'METHOD' : 0, 
               'PREDICATE' : [0] }
    processing.run('native:selectbylocation', parameters)
    outFeat = QgsFeature()
    selected = layer.selectedFeatures()
    for feature in selected:
        outFeat.setGeometry(feature.geometry())
        outFeat.setAttributes(feature.attributes())
        set_extent_layer.dataProvider().addFeatures([outFeat])
        set_extent_layer.updateExtents()
    set_extent_layer.commitChanges()
    return set_extent_layer


