import math
import arcpy
import numpy as np




def get_raster_coordinates(rc, ext, res):
  row = rc[0]
  col = rc[1]
  w = res[0]
  h = res[1]
  x = ext.XMin+w*col+w/2
  y = ext.YMax-h*row-h/2
  return x, y

def draw_line(cur, ij, dir, arrow_lenght, ext, res):
    horiz_len = arrow_lenght[0]
    diag_len = arrow_lenght[1]
    len = None
    if dir == 1:
        angle = 0
        len = horiz_len
    elif dir == 2:
        angle = -45/180 * math.pi
        len = diag_len
    elif dir == 4:
        angle = -90/180 * math.pi
        len = horiz_len
    elif dir == 8:
        angle = -135/180 * math.pi
        len = diag_len
    elif dir == 16:
        angle = math.pi
        len = horiz_len
    elif dir == 32:
        angle = 135/180 * math.pi
        len = diag_len
    elif dir == 64:
        angle = 90/180 * math.pi
        len = horiz_len
    elif dir == 128:
        angle = 45/180 * math.pi
        len = diag_len
    
    if len is not None:
        x, y = get_raster_coordinates(ij, ext, res)
        x0 = x - len/3.25 * math.cos(angle)
        y0 = y - len/3.25 * math.sin(angle)
        x1 = x + len/3.25 * math.cos(angle)
        y1 = y + len/3.25 * math.sin(angle)
        
        line = arcpy.Polyline(arcpy.Array([arcpy.Point(x0, y0), 
                                           arcpy.Point(x1, y1)]))
        
        cur.insertRow([line])