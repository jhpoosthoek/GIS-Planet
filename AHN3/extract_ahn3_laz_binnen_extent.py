##extentsf=vector
##lastools_folder=folder
##laz_folder=folder
##extent_buffer=number 0
##sf=boolean True

import os, sys
from osgeo import ogr
from qgis.core import *
from PyQt4.QtCore import *

output = os.path.join(laz_folder, os.path.basename(extentsf)[:-4] + "_xyzc.csv")

listfile = os.path.join(laz_folder, "list.txt")
os.chdir(laz_folder)

ds = ogr.Open(extentsf)
lyr = ds.GetLayer(0)
extent = lyr.GetExtent()

xmin = extent[0] - extent_buffer
xmax = extent[1] + extent_buffer
ymin = extent[2] - extent_buffer
ymax = extent[3] + extent_buffer

os.system("dir/b *.LAZ>list.txt")
if sf:
    command = '%s -lof list.txt -inside %s %s %s %s -single_points' % (os.path.join(lastools_folder, "las2shp"), xmin, ymin, xmax, ymax)
    os.system(command)
else:
    command = '%s -lof list.txt -inside %s %s %s %s -otxt -oparse xyzc' % (os.path.join(lastools_folder, "laszip"), xmin, ymin, xmax, ymax)
    os.system(command)

    f = open(listfile, "r")
    out = open(output, "w")
    out.write("X,Y,Z,CLASS\n")
    for filename in f:
        filename = filename.strip()[:-4] + ".txt"
        print filename

        file = open(filename, "r")
        for line in file:
            line = line.strip().split(" ")
            try:
                x = float(line[0])
                y = float(line[1])
                z = float(line[2])
                c = line[3]
                WRITE = 1
                if x > xmax:WRITE = 0
                if x < xmin:WRITE = 0
                if y > ymax:WRITE = 0
                if y < ymin:WRITE = 0
                if WRITE == 1:
                    out.write("%s,%s,%s,%s\n" % (x, y, z, c))
            except:
                pass
        file.close()
    out.close()
    f.close()