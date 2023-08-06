## Installation 
~~~bash
git clone https://gitlab.science.gc.ca/dlo001/radvelso.git
~~~
## Content and Usage

The following folders, scripts and files;

## 1. The folder /source_sqlite/ contains a sqlite file: 
   
   /source_sqlite/2019080106_ra (sqlite file with two VS) 

### 2. The folder /source_odim/ contains two odim files:
   
   /source_odim/CASBV_20190702_030003.qc.CASBV.h52 (sqlite file with one VS) 
   
   /source_odim/CASBV_20190702_031203.qc.CASBV.h5 (sqlite file with one VS) 
   
### 3. The folder /superobs/ contains script for superobbing:

In this folder there are two independent codes to make the average of the observations in the generation of the super observation. The codes are designed to work in parallel with a large sqlite file of  multiples VSs . But adaptation to other configurations is possible as it is modular. 

##### /superobs/superobs_sqlite.py

Code performing the search with sqlite and has as stages: 

 - Enter the sqlite file 

 - fill_ray ()^* create a map with the boxes where the average will be made ( shared program with superobs_numpy.py)

 - superobs () make a loop with each PPI 

 - average_boxes () search the observations and write the average of them in the new sqlite file with the super observation. 
  
Pros:

   - It has fewer stages and fewer lines. 
   - It is faster ~ 0.5 seconds per PPI 

 Cons:

  - Perhaps its conversion into Fortran is not so evident 
  - Knowledge of sqlite is required 



##### /superobs/superobs_numpy.py 

Code performing the search in data structures generated from a sqlite file and has as stages: 

 - Enter the sqlite file

 - fill_ray ()^* create a map with the boxes where the average will be made ( shared program with superobs_sqlite.py)
 - superobs () make a loop with each PPI 
 - read_sqlite_vol () transforms the PPI in sqlite into a data structure 
 - averaged_sqlite_dvel () searches in the data structure the observations per box and calculates the mean in a data structure 
 - to_sqlite () writes the data structure in the new sqlit file with the super observation. 

  Pros: 

  - Maybe the conversion  in Fortran is easier 
  - You need a basic knowledge of Sqlite only to read and write

  Cons: 

  - It is slower ~2 seconds per PPI
  - Contains more lines and stages 
 



##### /superobs/test_superobs.py
For validation, the tests have been done ( https://gitlab.science.gc.ca/dlo001/python-script-radar/blob/master/superobs/test_superobs.py ):

###### Test superobs_test_number_obs_boxes:

Creation of a map for visualizationing of each box where the average of the observations found will be calculated, showing in each box how many observations there are. Both codes have generated the same image independently. 

Same images: 

   - [`Figure from superobs_sqlite.py`](https://goc-dx.science.gc.ca/~dlo001/superobs/Opolar3_n20_10km_grid_fromsuperobs_2.png) 
              
   - [`Figure from superobs_numpy.py`](https://goc-dx.science.gc.ca/~dlo001/superobs/Opolar3_n20_10km_grid_fromsuperobs_2.png)
            
###### Run Test superobs_test_number_obs_boxes:

```shell
python test_superobs.py TestMethods.superobs_test1
there are 320 rays in the averaged PPI in 5 levels
First PPI 
Graphic analysis for superobservation (superobs_sqlite)
there are 320 rays in the averaged PPI in 5 levels
First PPI 
Graphic analysis for superobservation (superobs_numpy)
.
----------------------------------------------------------------------
Ran 1 test in 132.572s

OK
```


###### Test superobs_test_avg_sqlites: 

Generation of sqlite files with the average calculated for a certain configuration of fill_ray () both have generated the same sqlite file generating the same average of observations.

Same images: 

- [`Figure from superobs_sqlite.py`](https://goc-dx.science.gc.ca/~dlo001/sqlite_to_plot/figures/2019070206_ra_thin/sqlite_to_plot_sqlite_thin_0.4_20190702_30600.svg)
              
- [`Figure from superobs_numpy.py`](https://goc-dx.science.gc.ca/~dlo001/sqlite_to_plot/figures/2019070206_ra_thin2/sqlite_to_plot_sqlite_thin_0.4_20190702_30600.svg)
              
            

###### Run Test superobs_test_avg_sqlites:
```shell
python test_superobs.py TestMethods.superobs_test2
there are 320 rays in the averaged PPI in 5 levels
First PPI 
Time analysis for one PPI (superobs_sqlite)
Runtime total one PPI:  0.4667 s
there are 320 rays in the averaged PPI in 5 levels
First PPI 
Time analysis for one PPI (superobs_numpy)
Runtime total one PPI:  2.6713 s
.
----------------------------------------------------------------------
Ran 1 test in 8.777s

OK
```

###### Test total_number_obs:

Test of the total number of observations and total sum of observations on the tiles 

###### Test total_box:

Test funtion to make sure that azimuths and ranges are selected properly in the average

^* Boxes are generated without overlap, when tiles ray starts, it ends at the end of the last allowed value of the range. The boxes are defined by delta range and number of rays  to setup the size of the tile.

   
   
 

<!---
# Content

The following folders, scripts and files;

1. The folder /sqlite_to_plot/ contains script to visualize from a sqlite file:

    [`/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py`](/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py)
    
    /sqlite_to_plot/2019080106_ra (sqlite file before MIDAS)                 
    
    /sqlite_to_plot/2019080106_ra_midas (sqlite file after MIDAS)
    
    /sqlite_to_plot/2019080106_ra_midas_thin (sqlite file with thinning after MIDAS)
    
    [`/figures_to_plot/figures`](/sqlite_to_plot/figures)
    
2. The folder /omp/ contains script to calculate the BIAS and STDDEV as a function of range or height from a sqlite file(s) after being created in MIDAS:
  
    [`/omp/omp.py`](/omp/omp.py)
    
    [`/omp/midas/`](/omp/midas/) (path to sqlite file after MIDAS)
    
    [`/omp/midas_thin/`](/omp/midas_thin/) (path to sqlite file with thinning after MIDAS)
    
    [`/omp/figures_midas/`](/omp/figures_midas/) (result from sqlite file after MIDAS)
    
    [`/omp/figures_midas_thin/`](/omp/figures_midas_thin/) (result from sqlite file with thinning after MIDAS)

3. The folder /slant_radar_root/ contains script for generating a picture of intersections between 
model level and the radar beam with the number of root possible for a PPI from a file created in MIDAS:
   
    [`/slant_radar_root/slant_radar_root.py`](/slant_radar_root/slant_radar_root.py)
    
    [`/slant_radar_root/Blainville04.dat`](/slant_radar_root/Blainville04.dat) ( file with the position intersections between 
model level and the radar beam in Blainville by MIDAS, elevation 0.4 )

    [`/slant_radar_root/Blainville08.dat`](/slant_radar_root/Blainville08.dat) ( file with the position intersections between 
model level and the radar beam in Blainville by MIDAS, elevation 0.8 )
    
    [`/slant_radar_root/slant_radar_root_Blainville04.png`](/slant_radar_root/slant_radar_root_Blainville04.png) (result from Blainville04.dat)
    
    [`/slant_radar_root/slant_radar_root_Blainville08.png`](/slant_radar_root/slant_radar_root_Blainville08.png) (result from Blainville08.dat)
    
4. The folder /superobs/ contains script for thinning. Boxes are generated without overlap and equal area, when tiles ray starts, it ends at the end of the last allowed value of the range. The boxes are defined by delta range and delta azimuth to setup the size of the tile :

     [`/superobs/superobs.py`](/superobs/superobs.py)
   
     /superobs/2019080312_ra (sqlite file before MIDAS)  
     
     result of the different configurations of the thinning:
   
     [`/superobs/polar_11-25.png`](/superobs/polar_11-25.png) (thinning configuration; delta azimuth starts from 11.25 and delta range is 10000 m) 
    
     [`/superobs/polar_11-25_obs.png`](/superobs/polar_11-25_obs.png) (same configuration as the previous image but only the tiles with observation(s) are represented)
   
     [`/superobs/polar_7-5.png`](/superobs/polar_7-5.png) (thinning configuration; delta azimuth starts from 7.5 and delta range is 10000 m)
   
     [`/superobs/polar_7-5_obs.png`](/superobs/polar_7-5_obs.png) (same configuration as the previous image but only the tiles with observation(s) are represented)
     

# Requirements


- Python >= 3.6 (install from [conda][anaconda-scidocs] if necessary)
- ast
- cartopy
- dask 
- distributed
- geo_tools
- glob
- imageio 
- itertools 
- legs 
- matplotlib
- math 
- ntpath
- numpy
- os
- sqlite3 
- sys 
- subprocess 
- time 


# Usage

# 1. Installation

```shell
# From the *EC* network
git clone https://gitlab.science.gc.ca/dlo001/python-script-radar.git
```

# 2. Run script to visualize:

```shell
cd python-script-radar/sqlite_to_plot  # for sripts to visualize
```

The [`/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py`](/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py) makes images of the radar observation from a sqlite file before being used in MIDAS. It is also capable of generating git for the whole or part of the sqlite file.

```shell
# Run script to visualize from the *EC* network. With -sqlite  argument to activate options with a sqlite file before MIDAS
python sqlite_to_plot_observation_elevation_data_time.py -filein 2019080106_ra -sqlite
```
result: 
- plots: [`/sqlite_to_plot/2019080106_ra/`](/sqlite_to_plot/figures/2019080106_ra/)
 
- gif:  [`/sqlite_to_plot/2019080106_ra/2019080106_ra_gifsicle.gif`](/sqlite_to_plot/figures/2019080106_ra/2019080106_ra_gifsicle.gif ) 

The [`/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py`](/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py) makes images of the radar observation and background from a sqlite file after being used in MIDAS. It is also capable of generating git for the whole or part of the file.

```shell
# Run script to visualize from the *EC* network. With  -sqlite_midas  argument to activate options with a sqlite file after MIDAS
python sqlite_to_plot_elevation_data_time.py -filein 2019080106_ra_midas -sqlite_midas
```
- result: [`sqlite_to_plot/figures/2019080106_ra_midas/ `](/sqlite_to_plot/figures/2019080106_ra_midas/) 

- gif:  [`sqlite_to_plot/figures/2019080106_ra_midas/2019080106_ra_midas_gifsicle.gif `](/sqlite_to_plot/figures/2019080106_ra_midas/2019080106_ra_midas_gifsicle.gif) 

The [`/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py`](/sqlite_to_plot/sqlite_to_plot_elevation_data_time.py) makes images of the radar observation and background from a sqlite file with thinning file after being used in MIDAS. It is also capable of generating git for the whole or part of the file.

```shell
# Run script to visualize from the *EC* network. With -sqlite_midas_thin  argument to activate options with a sqlite file with thinning after MIDAS
python sqlite_to_plot_elevation_data_time.py -filein 2019080106_ra_midas_thin -sqlite_midas_thin
```
result: 
- plots:  [`/sqlite_to_plot/figures/2019080106_ra_midas_thin/`](/sqlite_to_plot/figures/2019080106_ra_midas_thin/) 
 
- gif:  [`/sqlite_to_plot/figures/2019080106_ra_midas_thin/2019080106_ra_midas_thin_gifsicle.gif`](/sqlite_to_plot/figures/2019080106_ra_midas_thin/2019080106_ra_midas_thin_gifsicle.gif ) 

# 3. Run script for calculating statistics.

```shell
# Run script for calculating statistics from the *EC* network
cd python-script-radar/omp  
```
- The [`omp.py`](/omp/omp.py) makes images of the BIAS and STDDEV as a function of range or height  from a sqlite file(s) after being used in MIDAS. 

```shell
# Run sript for calculating statistics from the *EC* network. With -path  argument to indicate the path to the file(s)
python omp.py -path /midas/    # path to sqlite from MIDAS
```

result from file sqlite:   [`/omp/figures_midas/`](/omp/figures_midas/)

```shell
# Run sript for calculating statistics  from the *EC* network. -path  argument to indicate the path to the file(s)
python omp.py -path /midas_thin/  # path to  sqlite with thinning from MIDAS
``` 

result from sqlite file with a thinning as [`/superobs/polar_7-5.png`](/superobs/polar_7-5.png): [`/omp/figures_midas_thin/`](/omp/figures_midas_thin/)
 
# 4. Run script for root analysis in the use of slant path in MIDAS.
  ```shell
cd python-script-radar/slant_radar_root  # for sript to root analysis 
```
- The  [`slant_radar_root.py`](/slant_radar_root/slant_radar_root.py)   makes a picture of a number of possible roots and the position lat/lon of the intersection between the model level and the slant trajectory for PPI from a file generated in MIDAS. 

```shell
# Run script to root analysis in the use of slant path in MIDAS from the *EC* network. With -filein argument to indicate the file used 
python slant_radar_root.py -filein Blainville04.dat
``` 

result:   [`/slant_radar_root/slant_radar_root_Blainville04.png`](/slant_radar_root/slant_radar_root_Blainville04.png)


```shell
# Run script to root analysis in the use of slant path in MIDAS from the *EC* network. With -filein argument to indicate the file used 
python slant_radar_root.py -filein Blainville08.dat
``` 

result:   [`/slant_radar_root/slant_radar_root_Blainville08.png`](/slant_radar_root/slant_radar_root_Blainville08.png)

# 5.Run script for thinning of the radar observation.
  ```shell
cd python-script-radar/superobs   # for sript for data thinning 
```
- The  [`superobs.py`](/superobs/superobs.py)  makes thinning of the radar observation. This program has different options. 

```shell
# Run script to generate a valid sqlite file for MIDAS with the chosen thinning from the *EC* network
python superobs.py -filein 2019072606_ra
```
result: 2019072606_ra_thin


 
 
```shell
# Run scripts for time analysis for a PPI from the *EC* network. With -ppi  argument to activate options the time analysis for only one PPI.
python superobs.py -filein 2019072606_ra -ppi
Time analysis for one PPI
Runtime total one PPI  1.2047 s
---------------------------------------------------------------------
Generation boxes           0.005  % 0.0001 s
Preparation sql            13.303 % 0.1603 s
Read header                0.008  % 0.0001 s
Loop of select & insert    86.42  % 1.0412 s
   Boxes                   2.29   % 0.0276 s
   Select                  69.68  % 0.8395 s
                number =   10665 avg= 7.871344585091371e-05
   Insert                  11.89  % 0.1432 s
                number =   2096 avg= 6.833162166030935e-05
End commint & close        0.269  % 0.0032 s
```

 ```shell
# Run scripts for graphic analysis of the chosen thinning (size boxes) from the *EC* network. With -ppi and -plot arguments to activate options the graphic analysis for only one PPI.
python superobs.py -filein 2019072606_ra -ppi -plot 
```     

Figures: Delta azimuth starts from 11.25 and delta range is 10000 m
https://goc-dx.science.gc.ca/~dlo001/superobs/Opolar3_n20_10km_gridb.png

[`Figure 1`](https://gitlab.science.gc.ca/dlo001/python-script-radar/blob/master/superobs/Opolar_n16_10km_grid090.png) 
[`Figure 2`](https://gitlab.science.gc.ca/dlo001/python-script-radar/blob/master/superobs/Opolar_n16_10km_grid.png) 

[anaconda-scidocs]: https://portal.science.gc.ca/confluence/pages/viewpage.action?pageId=30278663<!--- Comments are Fun --->
