#!/usr/bin/pyhon3

#to run a single test: superobs_test_avg_obs
#  python unittest_superobs.py TestMethods.test_superobs_fake_data


import unittest
import numpy as np
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt 
import domutils.geo_tools as geo_tools 
import domutils.legs as legs


class TestMethods(unittest.TestCase):

      def test_superobs_fake_data(self):

        ''' 
          test funtion to make sure that modifications in the branch do not affect the result 
          for fake source
        '''

        import numpy as np
        import sqlite3
        import os
        import radvelso
        import subprocess
        import time as tm
        import datetime
        import sys
        import numpy as geek  
        #Fake dataaa
        date = 20210101
        time = 101010
        id_stn = "CASXX"
        lat_radar = 45.7063
        lon_radar  = -73.85
        antenna_altitude = 0.
        nominal_elevation = 1.0
        range_start = 0.
        range_end = 0.
        nyquist = 1.
       
        #full path of radvelso module
        radvelso_dir = os.path.dirname(radvelso.__file__)
        #root path of radvelso package (one dir up from radvelso module)
        package_dir = os.path.dirname(radvelso_dir)

        

        # sqlite file from fake data
        #flush fileouts if it already exists
        pathfile_from_source=f"{package_dir}/radvelso/tests/test_result/sqlite_files/2021010112_ra"
        if os.path.isfile(pathfile_from_source):
          os.remove(pathfile_from_source)
        pathfile_superobs=f"{package_dir}/radvelso/tests/test_result/sqlite_files/{date}12_superobbed_fake_data.sqlite"

        if os.path.isfile(pathfile_superobs):
          os.remove(pathfile_superobs)
        #init fake data to sqlite file
        conn  = sqlite3.connect(pathfile_from_source)

        #full path of radvelso module
        radvelso_dir = os.path.dirname(radvelso.__file__)
        #root path of radvelso package (one dir up from radvelso module)
        package_dir = os.path.dirname(radvelso_dir)
        #full path of schema we are looking for
        schema_file = f'{package_dir}/radvelso/schema/schema'
        
        # shema to sqlite file
        if not os.path.isfile(schema_file):
          raise ValueError(f'schema_file: {schema_file} does not exist')
          return schema_file
        with open(schema_file) as f:
          schema = f.read()
        
        conn.executescript(schema)
        order_sql ="""CREATE TABLE info( NAME, DESCRIPTION, UNIT );"""
        conn.execute( order_sql)
        order_sql =""" insert into  info values('SUPEROBBING', 'OFF','-');"""
        conn.execute( order_sql)

        ranges = np.array([40000.,41000.,42000.])
        header_cmd = ''' INSERT INTO HEADER (
                           ID_OBS, CENTER_AZIMUTH, NYQUIST, CENTER_ELEVATION, 
                           LAT, LON, NOMINAL_PPI_ELEVATION, 
                           DATE, TIME, ID_STN, RANGE_START, RANGE_END, 
                           ANTENNA_ALTITUDE
                         )                         
                         VALUES 
                           (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''

        data_cmd   = ''' INSERT INTO DATA (
                           ID_DATA,  ID_OBS, RANGE, OBSVALUE, HALF_DELTA_AZIMUTH, HALF_DELTA_RANGE
                         )
                         VALUES
                           (?,?,?,?,?,?) '''
        source_azimuths  = np.array([0., 22.5, 45., 67.5 ,90., 112.5, 135, 157.5, 180., 202.5, 225.,
                                     247.5, 270., 292.5, 315, 337.5])
        source_obsvalues = np.array([5., 10., 15., 20., 25., 30., 35., 40. ,-5.,-10.,-15.,-20., 
                                    -25.,-30.,-35.,-40.,-45.])
        source_half_delta_azimuth = np.array([ 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 
                                               1., 1., 1., 1.])
        source_half_delta_range   = np.array([ 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                                               1., 1., 1., 1.])
     
        id_obs  = 1
        datas = enumerate(zip(source_azimuths, source_obsvalues, source_half_delta_azimuth, source_half_delta_range))
        for rr,(azimuth, obsvalue, half_delta_azimuth, half_delta_range) in datas:
          #insert into header
          header_values = (id_obs, azimuth, nyquist, nyquist, lat_radar, lon_radar, nominal_elevation,
                           str(date), str(time), id_stn, range_start, range_end, antenna_altitude)
          conn.execute(header_cmd, header_values)
          id_data=1
          for range_obs  in ranges: 
            obsvalue=obsvalue/id_data
            #insert into data
            data_values = (id_data, id_obs, range_obs, obsvalue, half_delta_azimuth, half_delta_range)
            conn.execute(data_cmd, data_values)
            id_data += 1
          
          id_obs +=1
        conn.commit()
        conn.close()

        #compute average for sqlite file with fake data
        center_time = os.path.basename(f'{pathfile_from_source}')[:10]
        center_time = datetime.datetime.strptime(center_time, '%Y%m%d%H')
        window_width = 6.0
        infile_list = [f'{pathfile_from_source}']
        desired_radar_list = "CASXX"
        pathout = f"{package_dir}/radvelso/tests/test_result/sqlite_files/"
        outfile_struc = '%Y%m%d%H_superobbed_fake_data.sqlite'
        timing = False
        ops_run_name = None
        n_rays = 20
        delta_range = 10000
        n_cpus = 1
        obs_percentage = 0
        radvelso.compute_average(center_time=center_time,
                                 window_width=window_width, 
                                 infile_list=infile_list,
                                 desired_radar_list=desired_radar_list,
                                 pathout=pathout,
                                 outfile_struc=outfile_struc,
                                 timing=timing,
                                 ops_run_name=ops_run_name,
                                 n_rays = n_rays,
                                 delta_range = delta_range,   
                                 n_cpus = n_cpus,
                                 obs_percentage = obs_percentage)

        
        #comparison between  average computation from code (superobs_sqlite) and result by hand 
        #                                                               (calculated_result_hand)
        conn = sqlite3.connect(pathfile_superobs)   
        order_sql = f"select  obsvalue from header natural join data ;"
        results = conn.execute(order_sql).fetchall()
        # expected result
        calculated_result_hand= np.array([2.7777, 5.5555,8.3333, 11.1111, 13.8888,  16.6666, 19.4444, 
             22.2222,  -2.7777, -5.5555, -8.3333, -11.1111, -13.8888, -16.6666, -19.4444, -22.2222])
        source_azimuths = np.array([         0.,   22.5,   45.,    67.5,     90.,    112.5,     135, 
              157.5,     180.,   202.5,    225.,    247.5,     270.,    292.5,      315,    337.5])

        calculated_result_hand = np.sort(calculated_result_hand)
        results = [result[0] for result in results]
        results = np.sort(results)

        print (f"Source of fake data is:{pathfile_from_source}")
        print (f"Source of superobbed for fake data is:{pathfile_superobs}")
        from tabulate import tabulate 

        col_headers = ["Expected", "Calculated", "Azimuths" ]

        merged_array = np.array([np.round(results,1), np.round(calculated_result_hand,1), source_azimuths]).T


        table = tabulate(merged_array , col_headers, floatfmt = ".2f")
 
        print(table)
        # comparation
        test_superobs_fake_data=  (np.allclose(calculated_result_hand,results,atol=1e-4))
        self.assertEqual(test_superobs_fake_data, True)


if __name__ == '__main__':
    unittest.main()
