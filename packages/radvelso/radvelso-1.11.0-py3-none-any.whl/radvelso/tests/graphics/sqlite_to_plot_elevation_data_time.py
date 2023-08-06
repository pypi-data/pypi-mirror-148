#!/usr/bin/python3
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import math 
import ast 
import sqlite3
import sys
import matplotlib as mpl
import os
import imageio
import cartopy.feature as cfeature
from itertools import chain
import domutils.legs as legs
import  domutils.geo_tools as geo_tools 
from subprocess import call
import domutils.radar_tools as radar_tools
from matplotlib import pyplot
import  matplotlib 
import gc
from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic
import copy

def sqlite_to_plot_elevation_data_time(filein,time,rele,folderout, sql,sqlthin, sqlmidas, sqlmidasthin ):
  """"
     Makes a picture of a plan position indicator (PPI)

     filein       :  sqlite file
     time         :  measurement time
     rele         :  elevation of the PPI
     folderout    :  folder where to generate images
     sql          :  if sql=true piture from a file sqlite
     sqlmidas     :  elif sqlmidas=true picture from a file sqlite after midas 
     sqlmidasthin :  elif sqlmidasthin=true picture from a file sqlite with thinning after midas
    ====================================
  """


  distance_radar = 240000                                                            #  [meters] Distance from the radar to the farthest point taken into account
  step_range     = 500                                                               #  [meters] Range step
  step_azimuth   = 0.5                                                               #  [-] Azimuth step   
  radius         = 6371000.                                                         #  Earth Radius
  re             = radius*(4./3.)

  azimuth_array  = np.arange(0.25,360,step_azimuth, dtype=float )            #  Azimuth  Array
 # range_array    = np.arange(127, 250000, 250, dtype=float)    #  Range distance Radar Array  

  
  range_array    = np.arange(12500, distance_radar , step_range, dtype=float)    #  Range distance Radar Array  
  matrix_obs     = np.full((len(azimuth_array),len(range_array)),-3333)              #  Observation matrix
  if ((sqlmidas==True) or (sqlmidasthin==True)): matrix_p = np.full((len(azimuth_array),len(range_array)),-3333)              #  P matrix
  matrix_lon     = np.zeros((len(azimuth_array),len(range_array)))                   #  longitud matrix
  matrix_lat     = np.zeros((len(azimuth_array),len(range_array)))                   #  latitud matrix  
  ring_array     = np.arange( 0., 250000.,50000.)                                    #  Ring of the grid line
  lon_ring_array = np.zeros(0)                                                       #  Ring lat array
  lat_ring_array = np.zeros(0)                                                       #  Ring lon array
  lon_ring_array2 = np.zeros(0)                                                       #  Ring lat array
  lat_ring_array2 = np.zeros(0)                                                       #  Ring lon array

  missing        = -9999.                                                            #  missing value
                                    
  # open sqlite
  ##################################
  conn = sqlite3.connect(filein)

  #  reding parametres of  Header
  ##################################
  order_sql =  " select lat,lon, ANTENNA_ALTITUDE, date, id_stn from  data header natural join header where abs(NOMINAL_PPI_ELEVATION-?)<0.1  and time=? limit 1"
  conn.row_factory = sqlite3.Row 
  cursor = conn.cursor()
  cursor.execute( order_sql ,(float(rele) ,int(time),))
  result = cursor.fetchone()
  id_stn = result['id_stn']
  lon  = math.radians(result['lon'])
  lat  = math.radians(result['lat'])
  elev = result['ANTENNA_ALTITUDE'] 
  date = result['date'] 
  ## filling the observation matrix 
  ##################################
  order_sql = "SELECT CENTER_AZIMUTH,range, obsvalue, omp, HALF_DELTA_AZIMUTH, HALF_DELTA_RANGE FROM data header  natural join header where abs(NOMINAL_PPI_ELEVATION-?)<0.1  and time=?"
  cursor = conn.cursor()
  for  rzam,vcoord, obsvalue, omp, delta_azm, delta_range in  cursor.execute( order_sql ,(float(rele) ,int(time),)):
     if (sql==True):
        i = (np.abs(azimuth_array - rzam)).argmin()
        j = (np.abs(range_array - vcoord)).argmin()
        matrix_obs[i,j] =  obsvalue 
     elif (sqlthin==True):
       i1 = (np.abs(azimuth_array - rzam-delta_azm)).argmin()
       i0 = (np.abs(azimuth_array - rzam+delta_azm)).argmin()
       j1 = (np.abs(range_array - vcoord-delta_range)).argmin()
       j0 = (np.abs(range_array - vcoord+delta_range)).argmin()
       if (i0==i1):
          matrix_obs[i0,j0:j1] = obsvalue
       else:
          matrix_obs[i0:i1,j0:j1] = obsvalue
     elif (sqlmidas==True):
        if (omp!=None):
           i = (np.abs(azimuth_array - rzam)).argmin()
           j = (np.abs(range_array - vcoord)).argmin()
           matrix_obs[i,j] = obsvalue  
           matrix_p[i,j]   = obsvalue - omp
     elif (sqlmidasthin==True):  

        if ((omp!=None)  ):

           i1 = (np.abs(azimuth_array - rzam-delta_azm)).argmin()
           i0 = (np.abs(azimuth_array - rzam+delta_azm)).argmin()
           j1 = (np.abs(range_array - vcoord-delta_range)).argmin()
           j0 = (np.abs(range_array - vcoord+delta_range)).argmin()
           if (i0==i1):
             matrix_p[i0,j0:j1] = obsvalue - omp
             matrix_obs[i0,j0:j1] = obsvalue
           else:
             matrix_p[i0:i1,j0:j1] = obsvalue - omp
             matrix_obs[i0:i1,j0:j1] = obsvalue

  
  # close sqlite
  #################################
  conn.close()

  # filling the lat-lon matrix 
  #################################
  for rzams in azimuth_array:
    
     for vcoord in range_array:
        
        i = (np.abs(azimuth_array - rzams)).argmin()
        j = (np.abs(range_array - vcoord)).argmin()
 
        rzam   = math.radians(rzams)
        radar_range  = vcoord
        #  distance from radar range


        d_radar = math.atan(radar_range*math.cos(math.radians(rele))/(radar_range*math.sin(math.radians(rele))+re+elev))*re
        #  second version -Book:Doppler Radar and Wheather Observation- --> 
       # d_radar = math.asin(radar_range*math.cos(math.radians(rele))/(radius+elev))*re    
        #  lat lon from  distance radar beam
        latSlant = math.asin( math.sin(lat)*math.cos(d_radar/radius) +
                   math.cos(lat)*math.sin(d_radar/radius)*math.cos(rzam))
        lonSlant = lon + math.atan2(math.sin(rzam)*math.sin(d_radar/radius)*math.cos(lat),
                   math.cos(d_radar/radius)-math.sin(lat)*math.sin(latSlant))
        latSlant = math.degrees(latSlant)
        lonSlant = math.degrees(lonSlant)

        #lonSlant,latSlant = geo_tools.lat_lon_range_az(result['lon'],result['lat'],radar_range/1000.,rzams)
        matrix_lon[i,j] = lonSlant
        matrix_lat[i,j] = latSlant
  
  
  # Configuration of the imagen
  ##################################
  mpl.rcParams['figure.dpi'] = 300
  mpl.rcParams['text.usetex']  = False
  mpl.rcParams['svg.fonttype'] = 'none'
  mpl.rcParams.update({'font.size': 18})

  # pixel density of image to plott

  ratio = 0.8
  hpix = 900.       #number of horizontal pixels
  vpix = ratio*hpix #number of vertical pixels
  imgRes = (int(hpix),int(vpix))
  center_lat = math.degrees(lat)
  center_lon = math.degrees(lon)

  #cartopy Rotated Pole projection
  pole_latitude=90.
  pole_longitude=0.
  proj = ccrs.RotatedPole(pole_latitude=pole_latitude, pole_longitude=pole_longitude)
                         
  mapExtent=[matrix_lon.min(), matrix_lon.max(), matrix_lat.min(), matrix_lat.max()]
  if ((sqlmidas==True) or (sqlmidasthin==True)): fig_w, fig_h = 9, 4. #size of figure
  if ((sql==True) or (sqlthin==True)) :  fig_w, fig_h = 7, 4.#size of figure
  fig = plt.figure(figsize=(fig_w, fig_h))
  rec_w = 3.1          #size of axes
  rec_h = 3.1          #size of axes
  sp_w  = 1.0          #horizontal space between axes
  sp_h  = 1.0          #vertical space between axes
  xp = .02               #coords of title (axes normalized coordinates)xy=(.1/rec_w, 3.7/rec_h)
  yp = 1.02

  # two color divergent mapping
  x0, y0 = 1.0/fig_w , .5/fig_h
  ax1 = fig.add_axes( [x0,y0,rec_w/fig_w,rec_h/fig_h],projection=proj)
  ax1.set_extent(mapExtent)
  if ((sqlmidasthin==True)): dum = ax1.annotate(str(id_stn)+' '+str(date)+' '+str(time)+'\nNominal elevation ='+str(round(rele,4))+' ',size=18,
                     xy=(xp, yp), xycoords='axes fraction')#  bbox=dict(boxstyle="round", fc='white', ec='white')
 
  if ((sqlmidas==True)):  dum = ax1.annotate(str(id_stn)+' '+str(date)+' '+str(time)+'\nNominal elevation ='+str(round(rele,4))+'\nRadar (QC)',size=18,
                     xy=(xp, yp), xycoords='axes fraction')#  bbox=dict(boxstyle="round", fc='white', ec='white')
 

# dum = ax1.annotate('Radar (QC) ' ,size=18,
#                      xy=(xp, yp), xycoords='axes fraction')#  bbox=dict(boxstyle="round", fc='white', ec='white')

  #format_axes(ax1)
  brown_purple=[[ 45,  0, 75],
                  [ 84, 39,136],
                  [128,115,172],
                  [188,181,220],
                  [216,218,235],
                  [247,247,247],
                  [254,224,182],
                  [253,184, 99],
                  [224,130, 20],
                  [179, 88,  6],
                  [127, 59,  8]]
   
  range_arr = [-48.,-40.,-30.,-20,-10.,-1.,1.,10.,20.,30.,40.,48.]
   #missing values
  missing  = -9999
  missing_color = 'grey_100'
  undetect = -3333.
  undetect_color = 'grey_170'

                
  
  projInds = geo_tools.ProjInds(src_lon= matrix_lon, src_lat=matrix_lat,extent=mapExtent, dest_crs=proj,
                                      extend_x=False, extend_y=True,image_res=imgRes, missing=missing )
  



  mappingPastel = legs.PalObj(range_arr=range_arr,
                                color_arr=brown_purple,                               
                                solid=    'supplied',
                                excep_val=[missing,undetect],
                                excep_col=[missing_color, undetect_color])
                                
  proj_data = projInds.project_data(matrix_obs )
  if ((sql==True) or (sqlthin==True)) : mappingPastel.plot_data(ax=ax1, data=proj_data, zorder=0,
                      palette='right', pal_units='Doppler velocity [m/s]', pal_format='{:3.0f}')
  if ((sqlmidas==True)  or  (sqlmidasthin==True)): mappingPastel.plot_data(ax=ax1, data=proj_data, zorder=0, pal_format='{:3.0f}')   #palette options

  # add political boundaries
  #add_feature(ax)
  ax1.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.1, edgecolor='0.1',zorder=1)
  ax1.add_feature(cfeature.LAKES.with_scale('10m'), linewidth=0.1, edgecolor='0.1',zorder=1)
  ax1.add_feature(cfeature.RIVERS.with_scale('10m'), linewidth=0.1, edgecolor='0.1',zorder=1)
  color=(100./256.,100./256.,100./256.)
  color2=(50./256.,50./256.,50./256.)
  #add a few azimuths lines
  az_lines = np.arange(0,360.,90.)
  ranges   = np.arange(250.)
  for this_azimuth in az_lines:
        lons, lats = geo_tools.lat_lon_range_az(result['lon'],result['lat'], ranges, this_azimuth)
        ax1.plot(lons, lats, transform=ccrs.PlateCarree(), c=color, zorder=300, linewidth=.3)#add a few range circles
  #add a few range circles
  ranges   = np.arange(0,250.,100.)
  azimuths = np.arange(0,361.)#360 degree will be included for full circles
  for this_range in ranges:
       lons, lats = geo_tools.lat_lon_range_az(result['lon'],result['lat'],  this_range, azimuths)
       ax1.plot(lons, lats, transform=ccrs.PlateCarree(), c=color, zorder=300, linewidth=.3)


#  ax1.scatter(lon_ring_array,lat_ring_array,transform=ccrs.PlateCarree(),marker='x',c='g', s=0.04)
#  ax1.scatter(np.degrees(lons),np.degrees(lats), transform=ccrs.PlateCarree() ,marker='o',c='g', s=0.04)

  if ((sqlmidas==True) or (sqlmidasthin==True)):
     x0, y0 = (.5+rec_w+sp_w)/fig_w , .5/fig_h
     ax2 = fig.add_axes([x0,y0,rec_w/fig_w,rec_h/fig_h],projection=proj)
     ax2.set_extent(mapExtent)
     dum = ax2.annotate('Model' , size=18,
                      xy=(xp, yp), xycoords='axes fraction')# bbox=dict(boxstyle="round", fc='white', ec='white'))
 #    dum = ax2.annotate('Model \nNominal elevation ='+str(round(rele,4)), size=12,
 #                      xy=(xp, yp), xycoords='axes fraction')# bbox=dict(boxstyle="round", fc='white', ec='white'))

     proj_data = projInds.project_data(matrix_p)
 
     mappingPastel = legs.PalObj(range_arr=range_arr,
                                color_arr=brown_purple,                               
                                solid=    'supplied',
                                excep_val=[missing,undetect],
                                excep_col=[missing_color, undetect_color])

     mappingPastel.plot_data(ax=ax2, data=proj_data, zorder=0,
                      palette='right', pal_units='Doppler velocity [m/s]', pal_format='{:3.0f}')
     # add political boundaries
     #add_feature(ax2)
     ax2.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.1, edgecolor='0.1',zorder=1)
     ax2.add_feature(cfeature.LAKES.with_scale('10m'), linewidth=0.1, edgecolor='0.2',zorder=1)
     ax2.add_feature(cfeature.RIVERS.with_scale('10m'), linewidth=0.1, edgecolor='0.2',zorder=1)
     #add a few azimuths lines
     az_lines = np.arange(0,360.,90.)
     ranges   = np.arange(250.)
     for this_azimuth in az_lines:
        lons, lats = geo_tools.lat_lon_range_az(result['lon'],result['lat'], ranges, this_azimuth)
        ax2.plot(lons, lats, transform=ccrs.PlateCarree(), c=color, zorder=300, linewidth=.3)#add a few range circles
     #add a few range circles
     ranges   = np.arange(0,250.,100.)
     azimuths = np.arange(0,361.)#360 degree will be included for full circles
     for this_range in ranges:
       lons, lats = geo_tools.lat_lon_range_az(result['lon'],result['lat'],  this_range, azimuths)
       ax2.plot(lons, lats, transform=ccrs.PlateCarree(), c=color, zorder=300, linewidth=.3)


  if (sql==True): text='sqlite'
  if (sqlthin==True): text='sqlite_thin'
  if (sqlmidas==True): text='sqlite_midas'
  if (sqlmidasthin==True): text= 'sqlite_midas_thin'
 # plt.tight_layout() 
  plt.savefig(folderout+'/sqlite_to_plot_'+str(text)+'_'+str(round(rele,4))+'_'+str(date)+'_'+str(time)+'.svg', format='svg', dpi=100, bbox_inches='tight')
  plt.savefig(folderout+'/sqlite_to_plot_'+str(text)+'_'+str(round(rele,4))+'_'+str(date)+'_'+str(time)+'.png', format='png', dpi=100, bbox_inches='tight')

  plt.show(block=False)
  plt.close(fig)
  gc.collect() 
  matplotlib.pyplot.figure().clear()
  matplotlib.pyplot.close()
  return text

def main(filein, sql,sqlthin, sqlmidas, sqlmidasthin):
   # open sqlite 
   conn2 = sqlite3.connect(filein)
   # creating array of time
   times = conn2.execute("select distinct TIME from header order by 1 ;").fetchall()
   times = np.array(ast.literal_eval(','.join(map(str,chain.from_iterable(times)))),dtype=int)
   # creating array of elevation
   reles = conn2.execute("select distinct NOMINAL_PPI_ELEVATION from header order by 1 ;").fetchall()
   reles = np.array(ast.literal_eval(','.join(map(str,chain.from_iterable(reles)))),dtype=float)
   
  # azimuth_array=conn2.execute("select distinct rzam from header where RELE=0.4 order by 1;").fetchall()
  # azimuth_array=np.array(ast.literal_eval(','.join(map(str,chain.from_iterable(azimuth_array)))),dtype=float)

  # range_array=conn2.execute("select distinct vcoord from data order by 1 ;").fetchall()
  # range_array= np.array(ast.literal_eval(','.join(map(str,chain.from_iterable(range_array)))),dtype=float)
#
   # close sqlite  
   conn2.close() 
   # Return the base name of pathname path 
   basename = os.path.basename(filein)
   # Return current working directory of a process
   path_pwd = os.getcwd()
   # folderout 
   folderout=path_pwd+"/figures/"+basename
   try:
      os.makedirs(folderout)
   except OSError: 
      print ("Creation of the directory %s failed"  % folderout)
   else:
      print ("Successfully created the directory %s " % folderout)

   print ("Executing sqlite_to_plot_elevation_data_time for all values")
 
   date=basename[0:8]
   # creating graphics
   for rele in reles[0:1]:
    for time in times:
    #  time=times

      text = sqlite_to_plot_elevation_data_time(filein, time, rele,folderout,sql,sqlthin, sqlmidas, sqlmidasthin)
      # creating gif
   for rele in reles[0:1]:
     images = []
     for time in times:

      file_name=folderout+'/sqlite_to_plot_'+str(text)+'_'+str(round(rele,4))+'_'+str(date)+'_'+str(time)+'.png'   
      file_path = os.path.join(folderout+"/", file_name)
      images.append(imageio.imread(file_path))
   # creating with imageio
   imageio.mimsave(folderout+"/"+basename+".gif", images, fps=55, duration=1)
   # compressing gif
   call(["gifsicle",  folderout+"/"+basename+".gif","-o",  folderout+"/"+basename+"_gifsicle.gif"])
if __name__ == '__main__':
   import argparse 
   print("Executing ")
   parser = argparse.ArgumentParser()
   parser.add_argument('-filein',  action="store", dest="filein",
        required=True, help=" sql file" , default="None")
   parser.add_argument('-sqlite', action="store_true", help="activation plot from sqlite file")
   parser.add_argument('-sqlite_thin', action="store_true", help="activation plot from sqlite file")
   parser.add_argument('-sqlite_midas', action="store_true", help="activation plot from sqlite after midas" )    
   parser.add_argument('-sqlite_midas_thin', action="store_true", help="activation plot from sqlite avec thinning after midas" )    
   args = parser.parse_args() 
   sql  = args.sqlite
   sqlthin      = args.sqlite_thin
   sqlmidas     = args.sqlite_midas
   sqlmidasthin = args.sqlite_midas_thin
  
main(args.filein, sql, sqlthin, sqlmidas, sqlmidasthin)
   

