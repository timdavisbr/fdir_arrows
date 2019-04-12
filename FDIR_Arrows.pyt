###################################################################################
# Name:       FDIR_Arrows: An arcpy toolbox module
# Purpose:    This module was developed as a final project for 
#             GISC 4500K - Application Development class. It takes a flow direction
#             raster and draws polylines in the direction of flow for user 
#             visualization. 
# 
# Author:     Timothy Davis
# Co-Authors: Dr. Huidae Cho, Zac Miller 
# Since:      April 2, 2019
###################################################################################


import math
import arcpy
import numpy as np 
from utils import draw_line


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [FlowDirectionArrows]

class FlowDirectionArrows(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Flow Direction Arrows"
        self.description = "This tool takes a flow direction raster and returns polylines in the direction of flow."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        fdir = arcpy.Parameter(
                name="fdir",
                datatype="GPRasterLayer",
                displayName="Flow Direction Raster",
                direction="Input",
                parameterType="Required",            
        )
        path_output = arcpy.Parameter(
                name="path_output",
                datatype="DEFolder",
                displayName="Output Folder",
                direction="Input",
                parameterType="Required",      
        )
        fc_name = arcpy.Parameter(
                name="fc_name",
                datatype="GPString",
                displayName="Feature Class Name",
                direction="Input",
                parameterType="Required",      
        )
        
        params = [fdir, path_output, fc_name]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        fdir_name = parameters[0].valueAsText
        path_output = parameters[1].valueAsText
        fc_name = parameters[2].valueAsText

        
     
        ras = arcpy.Raster(fdir_name)
        ras2 = arcpy.RasterToNumPyArray(ras)


        arrow_lenght = (ras.meanCellWidth, math.sqrt(ras.meanCellWidth**2 + ras.meanCellHeight**2))
        nrows = ras2.shape[0]
        ncol = ras2.shape[1]
        ext = ras.extent
        res = (ras.meanCellWidth, ras.meanCellHeight)
        arcpy.AddMessage(path_output)

        fc = arcpy.CreateFeatureclass_management(path_output, 
                                                 fc_name, 
                                                 'POLYLINE', 
                                                 None, 
                                                 None, 
                                                 None, 
                                                 ras.spatialReference)[0]

        with arcpy.da.InsertCursor(fc, ['SHAPE@']) as cur:
            for i in range(nrows):
                for j in range(ncol):
                    draw_line(cur, (i, j), 
                              ras2[i, j], 
                              arrow_lenght, 
                              ext, 
                              res)
        return
