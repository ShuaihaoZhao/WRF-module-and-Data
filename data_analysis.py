
#Compare the foracasted data with the real weather data

import pandas as pd

#make sure choosing the right alias
real_data=pd.read_csv(r'E:\U_of_A\ECE910\WRF_Data\WRF-module-and-Data\real_data\20200101.csv',
                      encoding = "ISO-8859-1", engine='python') 

forecasted_data=pd.read_csv(r'E:\U_of_A\ECE910\WRF_Data\WRF-module-and-Data\forecasted data\Edmonton_one_month.csv',
                      encoding = "ISO-8859-1", engine='python') 

print(forecasted_data.columns)#header names

part_real=real_data[['Temp (¡ãC)','Stn Press (kPa)','Wind Spd (km/h)']][0:742]# partial real data

part_forecasted=forecasted_data[['Temperature[Degree Celsius]','Surface Pressure [Pa]',
                                 '10m_X_Wind_Speed [m/s]','10m_Y_Wind_Speed [m/s]']];

                                 
#print(part_real.iterrows())
counter=0
error=0
for index,rows in part_real.iterrows():
    error=error+((part_forecasted.iloc[index,0]+273.15)-(part_real.iloc[index,0]+273.15))/(part_real.iloc[index,0]+273.15)
    counter+=1
    
print('Temperature mean percentage error: ',"%.4f" % round(error/counter, 4))
