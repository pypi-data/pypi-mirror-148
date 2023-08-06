# spacetimecube


Developed by Murat Çalışkan and Berk Anbaroğlu (c) 2022

## Examples of How To Use

Creating Random Points

```python
from spacetimecube import CreateRandomPoints

out_path = r"...\random_points.gpkg"

end = datetime.strptime('2015-02-02 23:59:59',"%Y-%m-%d %H:%M:%S")
start = datetime.strptime('2015-02-02 00:00:01',"%Y-%m-%d %H:%M:%S")

random_points = CreateRandomPoints(numberOfPoint=5000,
                                    maxDate=end,
                                    minDate=start,
                                    minWeight=0,
                                    maxWeight=1,
                                    minX=-74.0184326171875,
                                    maxX=-73.91214752197266,
                                    minY=40.70063018798828,
                                    maxY=40.87299346923828)

random_points.savePoints(path=out_path, driver="GPKG", layerName="ranfom_layer")

```

Creating Space Time Cube

```python
from spacetimecube import SpaceTimeCube

inputfilepath = "PG: host=%s dbname=%s user=%s password=%s" %(databaseServer,databaseName,databaseUser,databasePW)

outputfolderpath = r"..\output"

timefield = "time"
dateparser="%Y-%m-%d %H:%M:%S"
gridtype="size"
createtiff=True
weight=None
method="local_morans" # local_morans, getis_ord
gridsize=(10,10,10)

stc = SpaceTimeCube(inputfilepath=inputfilepath,
                    timefield=timefield,
                    outputfolderpath=outputfolderpath,
                    dateparser=dateparser,
                    method=method,
                    weight=weight,
                    gridsize=gridsize
                    )

stc.run()
```

Creating Plots

```python

from spacetimecube import PlotCube

points = PlotCube(r"..\points.csv")
# or
points = PlotCube(stc.points) 

points.plotTemporalChange(xcat=10, ycat=10, useweights=False)

points.plotNeighbors(xcat=10, ycat=10, tcat=10, useweights=False)
```
