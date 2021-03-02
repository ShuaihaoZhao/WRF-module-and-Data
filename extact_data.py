
from netCDF4 import Dataset
import numpy as np
from datetime import datetime
from datetime import timedelta
import pandas as pd
import math

data=Dataset(r'E:\U_of_A\ECE910\WRF_output\wrfout_one_month','r')
#print(data.variables.keys())#types of variables

lat=data.variables['XLAT'][0,:,0]
lon=data.variables['XLONG'][0,0,:]

#real-world location
lat_edmonton=53.5461
lon_edmonton=-113.4938

diff_lat=(lat-lat_edmonton)**2
diff_lon=(lon-lon_edmonton)**2

#find cloest longtitude and latitude
actual_lat = diff_lat.argmin()
actual_lon = diff_lon.argmin()

#set the time variable
start_time= data.variables['XTIME'].units[14:24] 
start_time= datetime.strptime(start_time, '%Y-%m-%d')#convert to datatime

time_step=int(data.variables['XTIME'][1])-int(data.variables['XTIME'][0])#60 mins
time_interval_num=len(data.variables['XTIME'][:])-1 #include the 0 index
end_time=start_time+timedelta(minutes=time_step*time_interval_num)
data_range=pd.date_range(start=start_time,end=end_time,periods=time_interval_num+1)

#Get mulitiple data values 
temperature_data = data.variables['T2']#in Kelvin 
x_wind_speed_data=data.variables['U10']#10-meter wind speed x
y_wind_speed_data=data.variables['V10']#10-meter wind speed y
pressure=data.variables['PSFC']#surface pressure
precipitation_RAINC=data.variables['RAINC']#RAINC is the rain calculation by cumulus scheme
precipitation_RAINNC=data.variables['RAINNC']#RAINNC is the rain calculation by microphysics scheme
humidity=data.variables['Q2']#2-meter specific humidity
sunshine_duration=data.variables['SWDOWN']
shortwave_radiation=data.variables['ACSWUPB']#Upwelling Surface Shortwave Radiation
longwave_radiation=data.variables['ACLWUPB']#Upwelling Surface Longwave Radiation

df=pd.DataFrame(0,columns=['Temperature[Degree Celsius]','10m_X_Wind_Speed [m/s]','10m_Y_Wind_Speed [m/s]',
                           'Surface Pressure [Pa]','Precipitatio(cumulus scheme)[kg/m2s1]',
                           'Precipitatio(microphysics scheme)[kg/m2s1]','Humidity',
                           'Sunshine Duration(short wave radiation>120 Wm2)[s]','Upwelling Surface Shortwave Radiation[W/m2]',
                           'Upwelling Surface Longwave Radiation[W/m2]'],index=data_range)#pandas data frame

for index in range(len(data_range)):
    df.iloc[index,0] = temperature_data[index, actual_lat, actual_lon]-273.15
    df.iloc[index,1] = x_wind_speed_data[index, actual_lat, actual_lon]
    df.iloc[index,2] = y_wind_speed_data[index, actual_lat, actual_lon]
    df.iloc[index,3] = pressure[index, actual_lat, actual_lon]
    df.iloc[index,4] = precipitation_RAINC[index, actual_lat, actual_lon]
    df.iloc[index,5] = precipitation_RAINNC[index, actual_lat, actual_lon]
    df.iloc[index,6] = humidity[index, actual_lat, actual_lon]  
    df.iloc[index,7] = sunshine_duration[index, actual_lat, actual_lon]
    df.iloc[index,8] = shortwave_radiation[index, actual_lat, actual_lon]
    df.iloc[index,9] = longwave_radiation[index, actual_lat, actual_lon]
    
#Save file into .csv file
df.to_csv('Edmonton_one_month.csv')



