from qgis.core import * 


from helper import *


QgsApplication.setPrefixPath("C:/Users/ASUS/AppData/Local/Temp/tmp4d4rmkcc.py", True)
# second argument to False disables the GUI.

qgs = QgsApplication([], False)


# Load providers

qgs.initQgis()


qgs.exitQgis()