#!/usr/bin/python3


import numpy as np
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt 
import domutils.geo_tools as geo_tools 
import domutils.legs as legs

def plot_ppi_test(sql_dict, id_stn, nominal_elevation,name_plot):

        '''
        plot dvel PPI found in a given  a dictionary which roughly mimics the structure of sqlite file

        Args:
           sql_dict:                 dictionary which roughly mimics the structure of sqlite file  
           id_stn:                   radar id_stn
           nominal_elevation:        desired nominal elevation.    
           name_plot:                desired name of the plot   
        Returns:
           None:                     plot dvel PPI  is save for desired  id_stn and nominal elevation
    
        '''


        # get data dictionary from sqlite file 
        radar_name = list(sql_dict.keys())
        for key in sql_dict[id_stn].keys():
             if isinstance(key, datetime.datetime):
                 ppi_date = key
                 break
        str_nominal_elevation = f'{nominal_elevation}'
        sql_dict = sql_dict[id_stn][ppi_date][str_nominal_elevation]         
        latitudes = sql_dict['latitudes']
        longitudes   = sql_dict['longitudes']
        doppvelocity =  sql_dict['obsvalue']

        #point density for figure
        mpl.rcParams['figure.dpi'] = 300
        # Use this for editable text in svg (eg with inkscape)
        mpl.rcParams['text.usetex']  = False
        mpl.rcParams['svg.fonttype'] = 'none'
        #size characters
        mpl.rcParams.update({'font.size': 18})

        #pixel density of image to plott
        ratio = 0.8
        hpix = 900.       #number of horizontal pixels
        vpix = ratio*hpix #number of vertical pixels
        imgRes = (int(hpix),int(vpix))

        #instantiate figure
        #all sizes are inches for consistency with matplotli
        fig_w, fig_h = 7, 4.#size of figure
        fig = plt.figure(figsize=(fig_w, fig_h))
        rec_w = 3.1          #size of axes
        rec_h = 3.1          #size of axes
        sp_w  = 1.0          #horizontal space between axes
        sp_h  = 1.0          #vertical space between axes
        xp = .02             #coords of title (axes normalized coordinates)xy=(.1/rec_w, 3.7/rec_h)
        yp = 1.02
        x0, y0 = 1.0/fig_w , .5/fig_h
       
        #cartopy Rotated Pole projection 
        pole_latitude=90.
        pole_longitude=0.
        map_extent=[ longitudes.min(), longitudes.max(), latitudes.min(), latitudes.max()]
        proj = ccrs.RotatedPole(pole_latitude=pole_latitude, pole_longitude=pole_longitude)

        #ax
        ax = fig.add_axes( [x0,y0,rec_w/fig_w,rec_h/fig_h],projection=proj)
        ax.set_extent(map_extent)
       
        #color mapping object for doppler velocity
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
        #plot non averaged data
        missing  = -9999
        missing_color = 'grey_100'
        undetect = -3333.
        undetect_color = 'grey_170'
        mappingPastel = legs.PalObj(range_arr=range_arr,
                                color_arr=brown_purple,                               
                                solid=    'supplied',
                                excep_val=[missing,undetect],
                                excep_col=[missing_color, undetect_color])

        #plot data & palette
        proj = ccrs.RotatedPole(pole_latitude=pole_latitude, pole_longitude=pole_longitude)
        projInds = geo_tools.ProjInds(src_lon= longitudes, src_lat=latitudes,extent=map_extent, dest_crs=proj,
                                      extend_x=False, extend_y=True,image_res=imgRes, missing=missing )
        proj_data = projInds.project_data(doppvelocity )
        mappingPastel.plot_data(ax=ax, data=proj_data, zorder=0,
                      palette='right', pal_units='Doppler velocity [m/s]', pal_format='{:3.0f}')

        #plot geographical and political boundaries in matplotlib axes
        ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.1, edgecolor='0.1',zorder=1)
        ax.add_feature(cfeature.LAKES.with_scale('10m'), linewidth=0.1, edgecolor='0.1',zorder=1)
        ax.add_feature(cfeature.RIVERS.with_scale('10m'), linewidth=0.1, edgecolor='0.2',zorder=1)
        ax.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.1, edgecolor='0.2',zorder=1)

        plt.savefig(f'{name_plot}', format='svg', dpi=100, bbox_inches='tight')
        plt.close(fig)
