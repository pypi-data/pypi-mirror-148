# -*- coding: utf-8 -*-


from osgeo import ogr, gdal, osr
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import product
import os, sys
from matplotlib import pyplot as plt

import warnings
warnings.filterwarnings("ignore")


class CreateRandomPoints:
    """
    Allows to create random points based on given parameters.
    
    Args:
        - **numberOfPoint** (*int*): Number of points to be created.
        - **minDate** (*datetime*): Minimum date to be assigned to the points.
        - **maxDate** (*datetime*): Maximum date to be assigned to the points.
        - **minX** (*float*): Minimum X (Longitude) coordinate of the points.
        - **maxX** (*float*): Maximum X (Longitude) coordinate of the points.
        - **minY** (*float*): Minimum Y (Latitude) coordinate of the points.
        - **maxY** (*float*): Maximum Y (Latitude) coordinate of the points.
        - **minWeight** (*float*): Minimum weight value to be assigned to the points.
        - **maxWeight** (*float*): Maximum weight value to be assigned to the points.
    
    Methods:
        - **savePoints**: Saves the created points to provided path. 
    
    """
    
    def __init__(self, numberOfPoint, minDate, maxDate, minX, maxX, minY, maxY, minWeight=0, maxWeight=1):
        assert maxWeight > minWeight, "Minimum weight is higher than maximum weight."
        assert maxDate > minDate, "Minimum date is higher than maximum date."
        
        self.NUMBER_OF_POINTS = numberOfPoint
        self.MIN_DATE = minDate
        self.MAX_DATE = maxDate
        self.MIN_WEIGHT = minWeight
        self.MAX_WEIGHT = maxWeight
        self.MIN_X = minX
        self.MAX_X = maxX
        self.MIN_Y = minY
        self.MAX_Y = maxY   
                        
        self.__dateDelta = int((self.MAX_DATE - self.MIN_DATE).total_seconds())
        self.__rnd_seconds = np.random.randint(0, self.__dateDelta, self.NUMBER_OF_POINTS)
        
        self.DATES = np.datetime64(self.MIN_DATE) + self.__rnd_seconds.astype("timedelta64[s]")       
        self.__long = np.random.rand(self.NUMBER_OF_POINTS) * (self.MAX_X - self.MIN_X) + self.MIN_X
        self.__lat = np.random.rand(self.NUMBER_OF_POINTS) * (self.MAX_Y - self.MIN_Y) + self.MIN_Y
        self.__weights = np.random.rand(self.NUMBER_OF_POINTS) * (self.MAX_WEIGHT - self.MIN_WEIGHT) + self.MIN_WEIGHT
        

    def savePoints(self, path, layerName = None, driver="ESRI Shapefile", crsCode=4326, crsWkt = None):
        """
        Saves the created points to provided path.
        
        Args:
            - **path** (*str*): path for created points to be saved.
            - **layerName** (*str*): path for created points to be saved.
            - **driver** (*str*): name of driver. Default is "ESRI Shapefile".
            - **crsCode** (*int*): EPSG code for output data.
            - **crsWkt** (*str*): CRS definition for output data. (If EPSG code is not provided.)
        """
        
        assert (crsCode is not None) or (crsWkt is not None), "One of the CRS options has to be provided."
        self.__srs = osr.SpatialReference()
        if crsCode:
            try:
                self.__res = self.__srs.ImportFromEPSG(crsCode)
                assert self.__res==0, "Invalid Code"
            except:
                raise Exception("Invalid Code")
                
        elif crsWkt:
            try:
                self.__res = self.__srs.ImportFromWkt(crsWkt)
                assert self.__res==0, "Invalid WKT"
            except:
                raise Exception("Invalid WKT")
                
        self.__drv = ogr.GetDriverByName(driver)
        self.__ds = self.__drv.CreateDataSource(path)
        self.__layer = self.__ds.CreateLayer("random_points" if layerName is None else layerName, self.__srs, ogr.wkbPoint)
        
        self.__layer.CreateField(ogr.FieldDefn("weight", ogr.OFTReal))
        self.__layer.CreateField(ogr.FieldDefn("X", ogr.OFTReal))
        self.__layer.CreateField(ogr.FieldDefn("Y", ogr.OFTReal))
        self.__dateField = ogr.FieldDefn("date", ogr.OFTString)
        self.__dateField.SetWidth(24)
        self.__layer.CreateField(self.__dateField)
        self.__defn = self.__layer.GetLayerDefn()
        
        for e,(x,y,w,t) in enumerate(zip(self.__long, self.__lat, self.__weights, self.DATES)):
            self.__feat = ogr.Feature(self.__defn)
            self.__feat.SetField('id', e)
            self.__feat.SetField('X', x)
            self.__feat.SetField('Y', y)
            self.__feat.SetField('weight', w)
            self.__feat.SetField("date", t.item().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Geometry            
            self.__geom = ogr.Geometry(ogr.wkbPoint)
            self.__geom.AddPoint(x, y)
            self.__feat.SetGeometry(self.__geom)    
            self.__layer.CreateFeature(self.__feat)
            self.__feat = None
            
        self.__ds = self.__layer = self.__defn = self.__feat = None
    

class PlotCube:
    """
    Allows to create plots.
    
    Args:
        - **points** (*str*): Path of the 'point.csv' file that is created.
    
    Methods:
        - **plotTemporalChange**: Plots the temporal change.
        - **plotNeighbors**: Plots the value of neighbors.    
    """
    
    def __init__(self, points):
        if os.path.isfile(points):
            self.INITPOINTS = np.genfromtxt(points, delimiter=',', skip_header=1, usecols=(0,1,2,3,4,5,6), dtype=np.float, encoding='utf-8')
            self.DATES = np.genfromtxt(points, delimiter=',', skip_header=1, usecols=(9), dtype=np.datetime64, encoding='utf-8')            
        else:
            self.INITPOINTS = points[:,:7]
            self.DATES = points[:,9]
    
    def __getNeighbors(self, points, x_cat, y_cat, t_cat, method="sum"):
        if (np.array([x_cat, y_cat, t_cat]) < 1).any():
            return None
        
        self.__x_cat_max, self.__y_cat_max, self.__t_cat_max = points[:,[4,5,6]].max(axis=0)
        if (x_cat > self.__x_cat_max) or (y_cat > self.__y_cat_max) or (t_cat > self.__t_cat_max):
            return None
            
        self.__neighbors = []
        self.__weights = []
        self.__relative_coors = defaultdict()
        self.__relative_coors_w = defaultdict()
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                for k in [-1,0,1]:
                    if (i != 0) or (j != 0) or (k != 0):
                        if ((np.array([y_cat+j, x_cat+i, t_cat+k]) > 0).all()) and (np.array([x_cat+i <= self.__x_cat_max, y_cat+j <= self.__y_cat_max, t_cat+k <= self.__t_cat_max]).all()):
                            self.__nb = np.array((points[:,4] == x_cat+i) & (points[:,5] == y_cat+j) & (points[:,6] == t_cat+k)).sum()
                           
                            if method=="median":
                                self.__r = points[(points[:,4] == x_cat+i) & (points[:,5] == y_cat+j) & (points[:,6] == t_cat+k)][:,3]
                                self.__w = np.median(self.__r) if self.__r.shape[0]>0 else 0
                            elif method=="mean":
                                self.__r = points[(points[:,4] == x_cat+i) & (points[:,5] == y_cat+j) & (points[:,6] == t_cat+k)][:,3]
                                self.__w = np.mean(self.__r) if self.__r.shape[0]>0 else 0
                            else:
                                self.__w = np.sum(points[(points[:,4] == x_cat+i) & (points[:,5] == y_cat+j) & (points[:,6] == t_cat+k)][:,3])
                                
                            self.__neighbors.append(self.__nb)
                            self.__weights.append(self.__w)
                            self.__relative_coors[(i,j,k)] = self.__nb
                            self.__relative_coors_w[(i,j,k)] = self.__w
        
        self.__relative_coors = sorted(self.__relative_coors.items(), key=lambda x:x[0][-1])
        self.__relative_coors_w = sorted(self.__relative_coors_w.items(), key=lambda x:x[0][-1])
        return self.__neighbors, self.__relative_coors, self.__weights, self.__relative_coors_w
        
    def plotTemporalChange(self, xcat, ycat, useweights=False):
        """
        Plots the temporal change.
        
        Args:
            - **xcat** (*int*): X axis of the categorical coordinate (coordinate of the cell of the cube).
            - **ycat** (*int*): Y axis of the categorical coordinate (coordinate of the cell of the cube).
            - **useweights** (*bool*): Take weights into consideration or not (Default is 'False').
        
        .. raw:: html

           <img src="../_static/temporal.svg" alt="temporal.svg" style="height: 300px;">
           
        """
        
        assert useweights in (True, False), "Invalid argument for useweights. Type 'True' or 'False' "
        self.__plot_points = self.INITPOINTS[:,[3,4,5,6]]
        try:
            self.__filtered_points = self.__plot_points[(self.__plot_points[:,1] == xcat) & (self.__plot_points[:,2] == ycat)]
            
            if useweights is False:
                self.__counts = np.array(np.unique(self.__filtered_points[:,3], return_counts=True)).T
            else:
                self.__unique_groups = np.unique(self.__filtered_points[:,3])
                self.__sums = []
                for group in self.__unique_groups:
                    self.__s = self.__filtered_points[(self.__filtered_points[:,3] == group)][:,0].sum()
                    self.__sums.append([group, self.__s])
                self.__counts = np.array(self.__sums)
            
            self.__title = str(self.DATES.min()) + (45 - len(str(self.DATES.max())) - len(str(self.DATES.min()))) * " " + str(self.DATES.max())
            
            self.__fig = plt.figure()
            if self.__counts.shape[0] != 0:
                self.__fig.clear()
                self.__ax = self.__fig.add_subplot(111)
                self.__ax.plot(self.__counts[:,0], self.__counts[:,1])
                self.__ax.scatter(self.__counts[:,0], self.__counts[:,1])
                                    
                self.__ax.grid(True)
                self.__ax.set_title(self.__title, loc="left")
                self.__ax.set_xlabel("Time")
                self.__ylabel = "Weighted Number of Points" if useweights is not False else "Number of Points"
                self.__ax.set_ylabel(self.__ylabel)
                self.__fig.tight_layout()
                plt.show()
            else:
                self.__fig.clear()
                self.__ax = self.__fig.add_subplot(111)
                self.__ax.grid(True)
                self.__ax.set_title(self.__title, loc="left")
                self.__ax.set_xlabel("Time")
                self.__ylabel = "Weighted Number of Points" if useweights is not False else "Number of Points"
                self.__ax.set_ylabel(self.__ylabel)
                self.__fig.tight_layout()
                plt.show()
                
        except Exception as e:
            print(e)

    def plotNeighbors(self, xcat, ycat, tcat, useweights=False):
        """
        Plots the temporal change.
        
        Args:
            - **xcat** (*int*): X axis of the categorical coordinate (coordinate of the cell of the cube).
            - **ycat** (*int*): Y axis of the categorical coordinate (coordinate of the cell of the cube).
            - **tcat** (*int*): T axis of the categorical coordinate (coordinate of the cell of the cube).
            - **useweights** (*bool*): Take weights into consideration or not (Default is 'False').
        
        .. raw:: html

           <img src="../_static/neighbors.svg" alt="temporal.svg" style="height: 300px;">
           
        """
        assert useweights in (True, False), "Invalid argument for useweights. Type 'True' or 'False' "
        
        self.__plot_points = self.INITPOINTS[:]
        self.__tcats = self.__plot_points[(self.__plot_points[:,4] == xcat) & (self.__plot_points[:,5] == ycat)][:,6]
        
        if self.__tcats.shape[0] == 0:
            print("There aren't any points in this cell!")
        elif tcat not in self.__tcats:
            print("Invalid 'tcat' paramter! Available parameters: {}".format(np.unique(self.__tcats)))
        else:
            self.__neighbors, self.__relative_coors, self.__weights, self.__relative_coors_w = self.__getNeighbors(self.__plot_points, xcat, ycat, tcat)
            
            if useweights is False:
                self.__current = ((self.__plot_points[:,4]==xcat) & (self.__plot_points[:,5]==ycat) & (self.__plot_points[:,6] == tcat)).sum()
                self.__coors = ["{},{},{}".format(*i[0]) for i in self.__relative_coors]
                self.__y = [i[1] for i in self.__relative_coors]
            else:
                self.__current = self.__plot_points[(self.__plot_points[:,4]==xcat) & (self.__plot_points[:,5]==ycat) & (self.__plot_points[:,6] == tcat)][:,3].sum()
                self.__current = round(self.__current,2)                
                self.__coors = ["{},{},{}".format(*i[0]) for i in self.__relative_coors_w]
                self.__y = [i[1] for i in self.__relative_coors_w]
            
            self.__colors = ["#8e8efa" if i.split(",")[-1]=="-1" else "#3939fa" if i.split(",")[-1]=="0" else "#14067d" for i in self.__coors]
            
            self.__x = range(2, len(self.__y)+2)
            self.__avg = round(sum(self.__y)/len(self.__y), 2)
            
            self.__title = "Number of Points in Neighbor Grids"
            
            self.__fig = plt.figure()            
            self.__ax = self.__fig.add_subplot(111)
            self.__ax.grid(True)
            
            self.__ax.bar([0], [self.__current], color = "red", label="Current Grid")
            self.__ax.bar([1], [self.__avg], color= "green", label="Average")
            self.__ax.bar(self.__x, self.__y, color = self.__colors)
            
            self.__xticks = [self.__current] + [self.__avg] + self.__coors
            self.__ax.set_xticks([0] + [1] + list(self.__x))
            self.__ax.set_xticklabels(self.__xticks, rotation=90)
            
            self.__ax.legend(fontsize="x-small")
            
            self.__ax.set_title(self.__title, loc="center")
            self.__ylabel = "Weighted Number of Points" if useweights is not False else "Number of Points"
            self.__ax.set_ylabel(self.__ylabel)
            self.__ax.set_xlabel("dx,dy,dt")
            self.__fig.tight_layout()

class SpaceTimeCube:
    """
    Allows to create Space Time Cube.
    
    Args:
        - **inputfilepath** (*str*): Path of the point file to be used for the analysis.
        - **timefield** (*str*): Name of time field.
        - **outputfolderpath** (*str*): Path of the output folder.
        - **aggregationmethod** (*str*): Method to be used to aggregate the weight of the points. (`mean`, `median`, `sum`)
        - **timestamptype** (*str*): Unit of timestamp (If timestamp is used as time variable). (`sec`, `milisec`)
        - **gridtype** (*str*): Method to be used to determine the size of the grid. (`size`, `interval`)
        - **gridsize** (*int/float*): Size of the grid. (If the gridtype is `size` gridsize is dimension of the cube. If the gridtype is `interval` gridsize is size of the cell)
        - **createtiff** (*bool*): Create tiff files or not.
        - **inputlayername** (*str*): Name of the layer to be used. If not provided default layer is used.
        - **dateparser** (*str*): If type of the time field to be used is string, this patern is used. If type of the time field is integer(timestamp) or datetime this variable is not necessary.
        - **weight** (*str*): Field to be used as weight.
        - **method** (*str*): Method to be used for analysis. (`getis_ord`, `local_morans`)
    
    Methods:
        - **getTimeFormatSamples**: Samples for dateparser.
        - **run**: Runs the analysis..
    
    Return:
        - **Grid**: Grids of study area in shapefile format.
        - **Points**: Input points with extra information in csv format.
        - **Analysis Results**: Getis Ord or Local Moran's I analysis results of the cells of the cubes in csv format.
        - **Tiff Files**: Getis Ord or Local Moran's I analysis results each time slice in tiff format.
    """
    
    def __init__(self, inputfilepath, timefield, outputfolderpath, aggregationmethod="sum", timestamptype="sec", gridtype="size",
                 gridsize=(10,10,10), createtiff=True, inputlayername=None, dateparser=None, weight=None, method="getis_ord"):
        self.WEIGHT = weight
        self.METHOD = method
        self.PATH = inputfilepath
        self.LAYERNAME = inputlayername
        self.DATEPARSER = dateparser
        self.TIMEFIELD = timefield
        self.TIMESTAMPTYPE = timestamptype
        self.GRIDTYPE = gridtype
        self.GRIDSIZE = gridsize
        self.CREATETIFF = createtiff
        self.OUTPUTFOLDER = outputfolderpath
        self.AGGREGATION = aggregationmethod
        
        assert self.METHOD in ('getis_ord', 'local_morans') , "Invalid method! Avaliable methods are 'getis_ord' and 'local_morans' "
    
    def getTimeFormatSamples(self):
        """
        Prints format samples for dateparser.
        """
        return [
                "%Y/%m/%d %H:%M:%S.%f",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M",
                "%Y/%m/%d %H",
                "%Y/%m/%d",
                "%Y/%m",
                "%Y",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d %H",
                "%Y-%m-%d",
                "%Y-%m",
                "%d/%m/%Y  %H:%M:%S.%f",
                "%d/%m/%Y  %H:%M:%S",
                "%d/%m/%Y  %H:%M",
                "%d/%m/%Y  %H",
                "%d/%m/%Y",
                "%d-%m-%Y  %H:%M:%S.%f",
                "%d-%m-%Y  %H:%M:%S",
                "%d-%m-%Y  %H:%M",
                "%d-%m-%Y  %H",
                "%d-%m-%Y"
                ]

    def __getDatetime(self, t):
        self.__ref_time = datetime.min
        self.__time_passed = timedelta(seconds=t)
        self.__dt = self.__ref_time + self.__time_passed
        return self.__dt  
    
    def __array2raster(self, newRasterSource, geotransform, srs, array):
        self.__cols = array.shape[1]
        self.__rows = array.shape[0]
    
        self.__driver = gdal.GetDriverByName('GTiff')
        self.__outRaster = self.__driver.Create(newRasterSource, self.__cols, self.__rows, 1, gdal.GDT_Float32)
        self.__outRaster.SetGeoTransform(geotransform)
        self.__outband = self.__outRaster.GetRasterBand(1)
        self.__outband.WriteArray(array)
        self.__outRaster.SetProjection(srs.ExportToWkt())
        self.__outband.FlushCache()
        del self.__outRaster, self.__outband
    
    def __createShp(self, gridx, gridy, out_folder, srs):
        self.__out_shp = os.path.join(out_folder, "grid.shp")
        self.__grid = []
        for i in range(1,len(gridx)):
            self.__minx = gridx[i-1]
            self.__maxx = gridx[i]    
            for j in range(1,len(gridy)):
                self.__miny = gridy[j-1]
                self.__maxy = gridy[j]
                self.__geom = f"POLYGON(({self.__minx} {self.__maxy}, {self.__maxx} {self.__maxy}, {self.__maxx} {self.__miny}, {self.__minx} {self.__miny}, {self.__minx} {self.__maxy}))"
                self.__grid.append([i, j, ogr.CreateGeometryFromWkt(self.__geom)])
                        
        self.__driver = ogr.GetDriverByName('Esri Shapefile')
        self.__ds = self.__driver.CreateDataSource(self.__out_shp)
        self.__layer = self.__ds.CreateLayer('grid', self.__srs, ogr.wkbPolygon)
        self.__layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        self.__layer.CreateField(ogr.FieldDefn('x_cat', ogr.OFTInteger))
        self.__layer.CreateField(ogr.FieldDefn('y_cat', ogr.OFTInteger))
        self.__defn = self.__layer.GetLayerDefn()
        
        for e, (i,j,g) in enumerate(self.__grid):
            self.__feat = ogr.Feature(self.__defn)
            self.__feat.SetField('id', e)
            self.__feat.SetField('x_cat', i)
            self.__feat.SetField('y_cat', j)
        
            # Geometry
            self.__feat.SetGeometry(g)    
            self.__layer.CreateFeature(self.__feat)
        
        self.__ds = self.__layer = self.__defn = self.__feat = None
                    
    def __points2csv(self, points, out_folder):
        self.__out_csv = os.path.join(out_folder, "points.csv")
        np.savetxt(self.__out_csv, points, delimiter=',',
                   header='x_coor, y_coor, t_coor, weight, x_cat, y_cat, t_cat, count, weighted_count, date',
                   fmt=('%.18e, %.18e, %.18e, %.18e, %d, %d, %d, %d, %.18e, %s'),
                   comments='')
        
    def __grid2csv(self, grids, out_folder):
        self.__stat = "getis_ord" if self.METHOD=="getis_ord" else "local_morans_I"
        self.__name = "grids_getis_ord.csv" if self.METHOD=="getis_ord" else "grids_local_morans_I.csv"
        self.__out_csv = os.path.join(out_folder, self.__name)
        np.savetxt(self.__out_csv, grids, delimiter=',',
                   header='x_cat, y_cat, t_cat, count, weighted_count, {}'.format(self.__stat),
                   fmt=('%d, %d, %d, %d, %.18e, %.18e'),
                   comments='')
            
    def run(self):
        """
        Executes the process.
        """
        self.__getDatetime_vec = np.vectorize(self.__getDatetime)
        
        self.__data = ogr.Open(self.PATH)
        self.__layer = self.__data.GetLayer() if self.LAYERNAME is None else self.__data.GetLayer(self.LAYERNAME)     
        self.__layerdefn = self.__layer.GetLayerDefn()        
        self.__srs = self.__layer.GetSpatialRef()
        
        for i in range(self.__layerdefn.GetFieldCount()):
            self.__field = self.__layerdefn.GetFieldDefn(i)
            if self.__field.GetName() == self.TIMEFIELD:
                self.__timefieldtype = self.__field.GetTypeName()
            if self.__field.GetName() == self.WEIGHT:
                self.__weightfieldtype = self.__field.GetTypeName()
        
        self.__px = np.array([])
        self.__py = np.array([])
        self.__pt = np.array([])
        self.__pw = np.array([])
        
        self.__ref_time = datetime.min
        
        self.__check_t = 0
        for feat in self.__layer:
            if feat.geometry().IsEmpty():
                continue
            self.__geom = feat.geometry()
            
            if self.__geom.GetGeometryName() == "POINT":
                self.coors = [self.__geom.GetPoint_2D()]
            elif self.__geom.GetGeometryName() == "MULTIPOINT":
                self.coors = [g.GetPoint_2D() for g in self.__geom]
            
            for __x, __y in self.coors:            
                if (self.WEIGHT is not None) and ((self.__weightfieldtype.lower().startswith("int")) or (self.__weightfieldtype.lower().startswith("real"))):
                    self.__w = feat.GetField(self.WEIGHT)
                    self.__w = float(self.__w)
                else:
                    self.__w = 1.0
                
                if self.__timefieldtype.lower().startswith("date"):
                    try:
                        self.__name = feat.GetFieldAsDateTime(self.TIMEFIELD)
                        self.__dt = datetime(*[int(d) for d in self.__name])
                        self.__t = (self.__dt - self.__ref_time).total_seconds()
                        self.__check_t = 1
                    except:
                        self.__t = None
                        break
                        
                elif (self.__timefieldtype.lower().startswith("int")) or (self.__timefieldtype.lower().startswith("real")):                    
                    try:
                        self.__t = feat.GetFieldAsDouble(self.TIMEFIELD)
                        if self.TIMESTAMPTYPE == "milisec":
                            self.__t = float(self.__t) / 1000
                        self.__check_t = 1
                    except:
                        self.__t = None
                        break
                else:
                    try:
                        self.__name = feat.GetField(self.TIMEFIELD)
                        self.__dt = datetime.strptime(self.__name, self.DATEPARSER)
                        self.__t = (self.__dt - self.__ref_time).total_seconds()
                        self.__check_t = 1
                    except:
                        self.__t = None
                        break                
                
                self.__px = np.append(self.__px, __x)
                self.__py = np.append(self.__py, __y)
                self.__pt = np.append(self.__pt, self.__t)
                self.__pw = np.append(self.__pw, self.__w)
            
        assert self.__check_t == 1, "Invalid or no date field! Check the field 'name' or 'dateparser'"
        
        self.__xmin = self.__px.min()
        self.__xmax = self.__px.max()        
        
        self.__ymin = self.__py.min()
        self.__ymax = self.__py.max()
        
        self.__tmin = self.__pt.min()
        self.__tmax = self.__pt.max()
        
        if self.GRIDTYPE == "size":
            self.__grid_size_x = self.GRIDSIZE[0]
            self.__grid_size_y = self.GRIDSIZE[1]
            self.__grid_size_t = self.GRIDSIZE[2]
        else:
            self.__xint = self.GRIDSIZE[0]
            self.__yint = self.GRIDSIZE[1]
            self.__tint = self.GRIDSIZE[2]
            
            self.__grid_size_x = int((self.__xmax - self.__xmin) / (self.__xint))
            self.__grid_size_y = int((self.__ymax - self.__ymin) / (self.__yint))
            self.__grid_size_t = int((self.__tmax - self.__tmin) / (self.__tint))              
        
        self.__gridx = np.linspace(self.__xmin, self.__xmax, self.__grid_size_x + 1)
        self.__xcat = np.digitize(self.__px, self.__gridx, right=True)        
        
        self.__gridy = np.linspace(self.__ymin, self.__ymax, self.__grid_size_y + 1)
        self.__ycat = np.digitize(self.__py, self.__gridy, right=True)
        
        self.__gridt = np.linspace(self.__tmin, self.__tmax, self.__grid_size_t + 1)
        self.__tcat = np.digitize(self.__pt, self.__gridt, right=True)        
    
        assert len(self.__gridt) > 1, "The interval of time window is too high for splitting. Please decrease the Time Window value!"
    
        self.__pdt = self.__getDatetime_vec(self.__pt)
        self.points = np.array([self.__px, self.__py, self.__pt, self.__pw, self.__xcat, self.__ycat, self.__tcat, self.__pdt]).T
        
        self.points = pd.DataFrame(self.points, columns = ['x_coor', 'y_coor', 't_coor', 'weight', 'x_cat', 'y_cat', 't_cat', 'date'])
        self.points[['x_coor', 'y_coor', 't_coor', 'weight']] = self.points[['x_coor', 'y_coor', 't_coor', 'weight']].astype(float)
        self.points[['x_cat', 'y_cat', 't_cat']] = self.points[['x_cat', 'y_cat', 't_cat']].astype(int).replace(to_replace=0, value=1)
                
        self.__points_group = self.points.groupby(["x_cat","y_cat","t_cat"])
        self.points.insert(7,"count", self.__points_group["x_coor"].transform("count"))
        self.points.insert(8,"weighted_count", self.__points_group["weight"].transform(self.AGGREGATION))
        
        self.__cube = self.points.groupby(["x_cat","y_cat","t_cat"]).agg({"count":"first", "weight":"first","weighted_count":"first"}).reset_index()
        self.__cube.set_index(self.__cube.x_cat.astype(str) + "_" + self.__cube.y_cat.astype(str)+ "_" + self.__cube.t_cat.astype(str), inplace=True, drop=True)
        self.__cube.insert(0, "coor", self.__cube.index)
              
        self.__neighbors = {}
        self.__cnt = 1
        
        if self.METHOD == "getis_ord":
            for i in range(-1,2):
                for j in range(-1,2):
                    for k in range(-1,2):
                        self.__coor_name = "n{}_coor".format(self.__cnt)
                        self.__count_name = "n{}_count".format(self.__cnt)
                        self.__w_count_name = "n{}_weighted_count".format(self.__cnt)
                        
                        self.__n1 = self.__cube.iloc[:,:0]
                        self.__n2 = ((self.__cube.x_cat + i).astype(str) + "_" + (self.__cube.y_cat + j).astype(str)+ "_" + (self.__cube.t_cat + k).astype(str)).to_frame(name="new_coor")
                        self.__n = self.__n1.join(self.__n2, how="left")
                        self.__n.reset_index(inplace=True)
                        self.__n.rename(columns={"index":"base_coor", "new_coor" : self.__coor_name}, inplace=True)                            
                        self.__n = self.__n.merge(self.__cube, how="left", left_on=self.__coor_name, right_on="coor").loc[:,['base_coor', self.__coor_name, 'count','weighted_count']]
                        self.__n.rename(columns={"count":self.__count_name, "weighted_count":self.__w_count_name}, inplace=True)
                        self.__n.set_index("base_coor", inplace=True)
                        
                        self.__neighbors["n{}".format(self.__cnt)] = self.__n
                        self.__cnt += 1
            
            for _,df in self.__neighbors.items():
                self.__cube = self.__cube.join(df)
                            
            if self.WEIGHT is None:
                self.__counts = [c for c in self.__cube.columns if ("_count" in c) and ("weighted" not in c)]
                self.__counts_cube = self.__cube.loc[:,self.__counts]
                self.__n_of_cells = self.__cube.shape[0]
                
                self.__x_mean = self.__cube.loc[:,"count"].sum() / self.__n_of_cells
                self.__numerator2 = self.__cube.loc[:,self.__counts].sum(axis=1) - self.__x_mean * self.__cube.loc[:,self.__counts].count(axis = 1)
                self.__s2 = np.sqrt((self.__cube.loc[:,"count"]**2).sum() / self.__n_of_cells - self.__x_mean**2)
                self.__denom12 = self.__n_of_cells * self.__cube.loc[:,self.__counts].count(axis = 1)
                self.__denom22 = (self.__cube.loc[:,self.__counts].count(axis = 1))**2
                self.__denom2 = (self.__denom12 - self.__denom22) / (self.__n_of_cells-1)
                self.__denominator2 = np.sqrt(self.__denom2) * self.__s2                
                self.__cube["getis_ord"] = self.__numerator2 / self.__denominator2
                
            else:
                self.__w_counts = [w for w in self.__cube.columns if "_weighted_count" in w]
                self.__w_counts_cube = self.__cube.loc[:,self.__w_counts]
                self.__n_of_cells = self.__cube.shape[0]
                
                self.__x_mean = self.__cube.loc[:,"weighted_count"].sum() / self.__n_of_cells
                self.__numerator2 = self.__cube.loc[:, self.__w_counts].sum(axis=1) - self.__x_mean * self.__cube.loc[:, self.__w_counts].count(axis = 1)
                self.__s2 = np.sqrt((self.__cube.loc[:,"weighted_count"]**2).sum() / self.__n_of_cells - self.__x_mean**2)
                self.__denom12 = self.__n_of_cells * self.__cube.loc[:, self.__w_counts].count(axis = 1)
                self.__denom22 = (self.__cube.loc[:, self.__w_counts].count(axis = 1))**2
                self.__denom2 = (self.__denom12 - self.__denom22) / (self.__n_of_cells - 1)
                self.__denominator2 = np.sqrt(self.__denom2) * self.__s2                
                self.__cube["getis_ord"] = self.__numerator2 / self.__denominator2
                
            self.__cube = self.__cube.loc[:,['coor', 'x_cat', 'y_cat', 't_cat', 'count', 'weighted_count', 'getis_ord']]            
            self.__cube.to_csv(os.path.join(self.OUTPUTFOLDER, "grids_getis_ord.csv"), index=False)       
            
        elif self.METHOD == "local_morans":
            for i in range(-1,2):
                for j in range(-1,2):
                    for k in range(-1,2):
                        if (np.array([i,j,k]) != 0).any():
                            self.__coor_name = "n{}_coor".format(self.__cnt)
                            self.__count_name = "n{}_count".format(self.__cnt)
                            self.__w_count_name = "n{}_weighted_count".format(self.__cnt)
                            
                            self.__n1 = self.__cube.iloc[:,:0]
                            self.__n2 = ((self.__cube.x_cat + i).astype(str) + "_" + (self.__cube.y_cat + j).astype(str)+ "_" + (self.__cube.t_cat + k).astype(str)).to_frame(name="new_coor")
                            self.__n = self.__n1.join(self.__n2, how="left")
                            self.__n.reset_index(inplace=True)
                            self.__n.rename(columns={"index":"base_coor", "new_coor" : self.__coor_name}, inplace=True)                            
                            self.__n = self.__n.merge(self.__cube, how="left", left_on=self.__coor_name, right_on="coor").loc[:,['base_coor', self.__coor_name, 'count','weighted_count']]
                            self.__n.rename(columns={"count":self.__count_name, "weighted_count":self.__w_count_name}, inplace=True)
                            self.__n.set_index("base_coor", inplace=True)
                            
                            self.__neighbors["n{}".format(self.__cnt)] = self.__n
                            self.__cnt += 1
            
            for _,df in self.__neighbors.items():
                self.__cube = self.__cube.join(df)
                            
            if self.WEIGHT is None:
                self.__n_of_cells = self.__cube.shape[0]
                self.__x_mean = (self.__cube["count"].sum() - self.__cube["count"]) / (self.__n_of_cells - 1)
                self.__counts = [c for c in self.__cube.columns if ("_count" in c) and ("weighted" not in c)]
                self.__counts_cube = self.__cube.loc[:,self.__counts]
                
                self.__s2_numerator_2 = (((self.__cube["count"] - self.__x_mean)**2).sum() - (self.__cube["count"] - self.__x_mean)**2)
                self.__s2_2 = self.__s2_numerator_2 / (self.__n_of_cells-1)
                self.__xi_2 = self.__cube.loc[:,"count"]                        
                self.__I1_2 = (self.__xi_2 - self.__x_mean) / self.__s2_2
                self.__I2_2 = self.__counts_cube.subtract(self.__x_mean.values, axis=0).sum(axis=1)                            
                self.__I_2 = self.__I1_2 * self.__I2_2
                
                self.__ei_2 = self.__counts_cube.count(axis=1) / (self.__n_of_cells-1)
                self.__b2i_numerator_2 = ((self.__cube["count"] - self.__x_mean)**4).sum() - (self.__cube["count"] - self.__x_mean)**4
                self.__b2i_denominator_2 = self.__s2_numerator_2**2
                self.__b2i_2 = self.__b2i_numerator_2 / self.__b2i_denominator_2
                self.__B_numerator_2 = (2 * self.__b2i_2 - self.__n_of_cells) * self.__counts_cube.count(axis=1)**2
                self.__B_2 = self.__B_numerator_2 / ((self.__n_of_cells - 1) * (self.__n_of_cells - 2))
                self.__A_numerator_2 = (self.__n_of_cells - self.__b2i_2) * (self.__counts_cube.count(axis=1))
                self.__A_2 = self.__A_numerator_2 / (self.__n_of_cells - 1)
                self.__ei2_2 = self.__A_2 - self.__B_2
                self.__vi_2 = self.__ei2_2 - self.__ei_2**2
                self.__zi_2 = (self.__I_2 - self.__ei_2) / np.sqrt(self.__vi_2)
                self.__cube["local_morans_I"] = self.__zi_2
            
            else:
                self.__n_of_cells = self.__cube.shape[0]
                self.__x_mean = (self.__cube["weighted_count"].sum() - self.__cube["weighted_count"]) / (self.__n_of_cells - 1)
                self.__w_counts = [w for w in self.__cube.columns if "_weighted_count" in w]
                self.__counts_cube = self.__cube.loc[:,self.__w_counts]
                
                self.__s2_numerator_2 = (((self.__cube["weighted_count"] - self.__x_mean)**2).sum() - (self.__cube["weighted_count"] - self.__x_mean)**2)
                self.__s2_2 = self.__s2_numerator_2 / (self.__n_of_cells-1)
                self.__xi_2 = self.__cube.loc[:,"weighted_count"]
                self.__I1_2 = (self.__xi_2 - self.__x_mean) / self.__s2_2
                self.__I2_2 = self.__counts_cube.subtract(self.__x_mean.values, axis=0).sum(axis=1)     
                self.__I_2 = self.__I1_2 * self.__I2_2
               
                self.__ei_2 = self.__counts_cube.count(axis=1) / (self.__n_of_cells-1)
                self.__b2i_numerator_2 = ((self.__cube["weighted_count"] - self.__x_mean)**4).sum() - (self.__cube["weighted_count"] - self.__x_mean)**4
                self.__b2i_denominator_2 = self.__s2_numerator_2**2
                self.__b2i_2 = self.__b2i_numerator_2 / self.__b2i_denominator_2
                self.__B_numerator_2 = (2 * self.__b2i_2 - self.__n_of_cells) * self.__counts_cube.count(axis=1)**2
                self.__B_2 = self.__B_numerator_2 / ((self.__n_of_cells - 1) * (self.__n_of_cells - 2))
                self.__A_numerator_2 = (self.__n_of_cells - self.__b2i_2) * (self.__counts_cube.count(axis=1))
                self.__A_2 = self.__A_numerator_2 / (self.__n_of_cells - 1)
                self.__ei2_2 = self.__A_2 - self.__B_2
                self.__vi_2 = self.__ei2_2 - self.__ei_2**2
                self.__zi_2 = (self.__I_2 - self.__ei_2) / np.sqrt(self.__vi_2)                
                self.__cube["local_morans_I"] = self.__zi_2
                
            self.__cube = self.__cube.loc[:,['coor', 'x_cat', 'y_cat', 't_cat', 'count', 'weighted_count', 'local_morans_I']]                
            self.__cube.to_csv(os.path.join(self.OUTPUTFOLDER, "grids_local_morans_I.csv"), index=False)
        
        else:
            sys.exit("Invalid method!")
        
        self.points.to_csv(os.path.join(self.OUTPUTFOLDER, "points.csv"), index=False)
        
        del self.__data
                
        self.__x_max, self.__y_max, self.__t_max = self.points[['x_cat', 'y_cat', 't_cat']].astype(int).max(axis=0)
        self.__cells_of_cube = np.array(list(product(range(1,self.__x_max+1), range(1,self.__y_max+1), range(1,self.__t_max+1))))
        
        self.__cube_dim = pd.DataFrame(self.__cells_of_cube, columns=["x_cat","y_cat","t_cat"])
        
        self.__merged = pd.merge(self.__cube_dim, self.__cube, how="left",left_on=["x_cat","y_cat","t_cat"], right_on=["x_cat","y_cat","t_cat"])        
       
        if self.CREATETIFF:
            self.__stat_name = "getis_ord" if self.METHOD=="getis_ord" else "local_morans_I"
            self.__getis_res = self.__merged.loc[:,["x_cat","y_cat","t_cat",self.__stat_name]]
            self.__getis_groupped = self.__getis_res.groupby("t_cat")
            self.__result_cube = {}
            
            for i,df in self.__getis_groupped:
                self.__val = np.flipud(df.pivot(index="y_cat", columns="x_cat", values=self.__stat_name))
                self.__result_cube[i] = self.__val
            
            self.__gt0 = self.__gridx.min()
            self.__gt1 = self.__gridx[1] - self.__gridx[0]
            self.__gt2 = 0
            self.__gt3 = self.__gridy.max()
            self.__gt4 = 0
            self.__gt5 = self.__gridy[0] - self.__gridy[1]
            
            self.__geotransform = (self.__gt0, self.__gt1, self.__gt2, self.__gt3, self.__gt4, self.__gt5)
            
            self.__diff = int(self.__gridt[1] - self.__gridt[0])
            
            for i, ras in self.__result_cube.items():
                self.__name = str(self.__diff*(i))
                self.__newRasterName = r"g{}_{}.tiff".format(str(i).zfill(len(str(len(self.__result_cube.keys())))), self.__name)
                self.__newRasterSource = os.path.join(self.OUTPUTFOLDER, self.__newRasterName)                
                self.__array2raster(self.__newRasterSource, self.__geotransform, self.__srs, ras)
        
        self.__createShp(self.__gridx, self.__gridy, self.OUTPUTFOLDER, self.__srs)
