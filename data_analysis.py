
#Compare the foracasted data with the real weather data

import pandas as pd
import matplotlib.pyplot as plt
import math

#make sure choosing the right alias
real_data=pd.read_csv(r'E:\U_of_A\ECE910\WRF_Data\WRF-module-and-Data\real_data\20200101.csv',
                      encoding = "ISO-8859-1", engine='python') 

forecasted_data=pd.read_csv(r'E:\U_of_A\ECE910\WRF_Data\WRF-module-and-Data\forecasted data\Edmonton_one_month.csv',
                      encoding = "ISO-8859-1", engine='python') 

#print(forecasted_data.columns)#header names

#time=forecasted_data[['Unnamed: 0']]
part_real=real_data[['Temp (¡ãC)','Stn Press (kPa)','Wind Spd (km/h)']][0:742]# partial real data

part_forecasted=forecasted_data[['Temperature[Degree Celsius]','Surface Pressure [Pa]',
                                 '10m_X_Wind_Speed [m/s]','10m_Y_Wind_Speed [m/s]']];
                                 
#######################################################################Temperature

#plt.figure(figsize=(20,10))
#plt.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,0],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,0],label='real');
#
#plt.title('Real Temperature vs Forecasted Temperature')
#plt.xlabel('Time')
#plt.ylabel('Temperature (Kelvin)')
#plt.legend(loc="upper left")
#plt.show()

#######################################################################Pressure
#plt.figure(figsize=(20,10))
#plt.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,1],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,1]*1000,label='real');
#
#plt.title('Real Pressure vs Forecasted Pressure')
#plt.xlabel('Time')
#plt.ylabel('Pressure (Pa)')
#plt.legend(loc="upper left")
#plt.show()

#######################################################################Wind
wind=[]

for index_f,rows in part_forecasted.iterrows():
    wind.append((math.sqrt(part_forecasted.iloc[index_f,2]**2+part_forecasted.iloc[index_f,3]**2)/1000)*3600)

part_forecasted('Wind')=wind
#df_1=pd.DataFrame(wind,col)

#plt.figure(figsize=(20,10))
#plt.plot(forecasted_data.iloc[:,0],wind[:,0],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,2],label='real');
#
#plt.title('Real Wind Speed vs Forecasted Wind Speed')
#plt.xlabel('Time')
#plt.ylabel('Wind Speed [km/h]')
#plt.legend(loc="upper left")
#plt.show()
    
#######################################################################    
#counter=0
#error=0#temperature
#error_1=0#pressure
#error_2=0#wind Using Relative Percent Difference
#for index,rows in part_real.iterrows():
#    error=error+((part_forecasted.iloc[index,0]+273.15)-(part_real.iloc[index,0]+273.15))/(part_real.iloc[index,0]+273.15)
#    error_1=error_1+abs((part_forecasted.iloc[index,1])-(part_real.iloc[index,1])*1000)/(part_real.iloc[index,1]*1000)
#    error_2=error_2+2*abs((wind[index,0])-(part_real.iloc[index,2]))/((part_real.iloc[index,2])+(wind[index,0]))
#    counter+=1
#    
#print('Temperature mean percentage error: ',"%.4f" % round(error/counter, 4))
#print('Pressure mean percentage error: ',"%.4f" % round(error_1/counter, 4))
#print('Wind speed mean percentage error: ',"%.4f" % round(error_2/counter, 4))
#######################################################################



