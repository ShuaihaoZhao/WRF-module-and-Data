
#Compare the foracasted data with the real weather data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import seaborn as sns
import statistics
pd.options.mode.chained_assignment = None  # default='warn'

#make sure choosing the right alias
real_data=pd.read_csv(r'E:\U_of_A\ECE910\WRF_Data\WRF-module-and-Data\real_data\20200101.csv',
                      encoding = "ISO-8859-1", engine='python') 

new_data=pd.read_csv(r'E:\U_of_A\ECE910\WRF_Data\WRF-module-and-Data\real_data\blatchford_202101.csv',
                      encoding = "ISO-8859-1", engine='python')

forecasted_data=pd.read_csv(r'E:\U_of_A\ECE910\WRF_Data\WRF-module-and-Data\forecasted data\Edmonton_CONUS_d02.csv',
                      encoding = "ISO-8859-1", engine='python') 

print(real_data.columns)#header names

part_real=real_data[['Temp (¡ãC)','Stn Press (kPa)','Wind Spd (km/h)','Precip. Amount (mm)','Rel Hum (%)']][0:742]# partial real data

part_forecasted=forecasted_data[['Temperature[Degree Celsius]','Surface Pressure [Pa]',
                                 '10m_X_Wind_Speed [m/s]','10m_Y_Wind_Speed [m/s]']];
part_new=new_data[['humidity','irradiance','cloudcover']][0:741]                  
                                
#######################################################################Temperature

#fig, ax = plt.subplots(1,1,figsize=(15,10))
#
#ax.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,0],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,0],label='real');
#
#ticker_spacing = forecasted_data.iloc[:,0]
#ticker_spacing = 100
#ax.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
#plt.xticks(rotation = 45)
#
#plt.title('Real Temperature vs Forecasted Temperature')
#plt.xlabel('Time')
#plt.ylabel('Temperature (Â°C)')
#plt.legend(loc="upper left")
#plt.show()


#
########################################################################Pressure
fig, ax = plt.subplots(1,1,figsize=(15,10))
ax.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,1],label='forecasted')
plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,1]*1000,label='real');


ticker_spacing = forecasted_data.iloc[:,0]
ticker_spacing = 100
ax.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
plt.xticks(rotation = 45)

plt.title('Real Pressure vs Forecasted Pressure')
plt.xlabel('Time')
plt.ylabel('Pressure (Pa)')
plt.legend(loc="upper left")
plt.show()

########################################################################Wind
##
part_forecasted['Wind[km/h]']=((np.sqrt(part_forecasted['10m_X_Wind_Speed [m/s]']**2+part_forecasted['10m_Y_Wind_Speed [m/s]']**2)/1000.0)*3600.0)
##
#plt.figure(figsize=(20,10))
#plt.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,4],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,2],label='real');
#
#plt.title('Real Wind Speed vs Forecasted Wind Speed')
#plt.xlabel('Time')
#plt.ylabel('Wind Speed [km/h]')
#plt.legend(loc="upper left")
#plt.show()
#    
########################################################################    
#part_forecasted['precipitation[mm]']=forecasted_data.iloc[:,5]+forecasted_data.iloc[:,6]
part_forecasted['precipitation[mm]']=np.nan
for index_f,rows in forecasted_data.iterrows():
    if index_f>=1:
        part_forecasted.iloc[index_f,5]=forecasted_data.iloc[index_f,5]+forecasted_data.iloc[index_f,6]-(forecasted_data.iloc[index_f-1,5]+forecasted_data.iloc[index_f-1,6])
    else:
        part_forecasted.iloc[index_f,5]=forecasted_data.iloc[index_f,5]+forecasted_data.iloc[index_f,6]
        
#plt.figure(figsize=(20,10))
#plt.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,5],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,3],label='real');
#
#plt.title('Real Precipitation vs Forecasted Precipitation')
#plt.xlabel('Time')
#plt.ylabel('precipitation[mm]')
#plt.legend(loc="upper left")
#plt.show()                                
                                 
########################################################################humidity
part_forecasted['relative humidity']=np.nan
#es=0#saturation vapour pressure
#ws=0#mixing ratio
pq0 = 379.90516
a2 = 17.2693882
a3 = 273.16
a4 = 35.86
for index_r,rows in forecasted_data.iterrows():
#    es=0.6113*math.exp(5423*((1/273.15)-(1/(part_forecasted.iloc[index_r,0]+273.15))))
#    ws=0.622*(es/((part_forecasted.iloc[index_r,1]/1000)-es))
#    part_forecasted.iloc[index_r,6]=(forecasted_data.iloc[index_r,7]/ws)*100
    part_forecasted.iloc[index_r,6]=(forecasted_data.iloc[index_r,7]*100)/((pq0/part_forecasted.iloc[index_r,1])*np.exp(a2*(part_forecasted.iloc[index_r,0]-a3)/(part_forecasted.iloc[index_r,1]-a4)))
    
#    
#plt.figure(figsize=(20,10))
#plt.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,6],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0],part_real.iloc[:,4],label='real');
#
#plt.title('Real Relative Humidity vs Forecasted Relative Humidity')
#plt.xlabel('Time')
#plt.ylabel('Relative Humidity[%]')
#plt.legend(loc="upper left")
#plt.show()       
    
    
########################################################################solar irradiation
part_forecasted['irradiance']=np.nan
for index_i,rows in forecasted_data.iterrows():
    if index_i>0:
        part_forecasted.iloc[index_i,7]=(forecasted_data.iloc[index_i,11]-forecasted_data.iloc[index_i-1,11])/3600
    else:
        part_forecasted.iloc[index_i,7]=forecasted_data.iloc[index_i,11]/3600
       
#adjust solar irradiance H=H0(1-0.75n^3.4)
part_new['adj_irradiance']=np.nan
for i,rows in part_new.iterrows():
        part_new.iloc[i,3]= part_new.iloc[i,1]*(1-0.6* (part_new.iloc[i,2]/100.0))


#plt.figure(figsize=(20,10))
#plt.plot(forecasted_data.iloc[:,0],part_forecasted.iloc[:,7],label='forecasted')
#plt.plot(forecasted_data.iloc[:,0][1:742],part_new.iloc[:,3],label='real');
#plt.title('Real irradiance vs Forecasted  irradiance')
#plt.xlabel('Time')
#plt.ylabel(' irradiance[w m-2]')
#plt.legend(loc="upper left")
#plt.show()  
        
########################################################################
counter=0
error=0#temperature
error_1=0#pressure
error_2=0#wind Using Relative Percent Difference
error_3=0#precipitation
for index,rows in part_real.iterrows():
    error=error+abs((part_forecasted.iloc[index,0]+273.15)-(part_real.iloc[index,0]+273.15))/abs(part_real.iloc[index,0]+273.15)
    error_1=error_1+abs((part_forecasted.iloc[index,1])-(part_real.iloc[index,1])*1000)/(part_real.iloc[index,1]*1000)
    error_2=error_2+2*abs((part_forecasted.iloc[index,4])-(part_real.iloc[index,2]))/abs((part_real.iloc[index,2])+(part_forecasted.iloc[index,4]))
#    error_3=error_3+2*abs((part_forecasted.iloc[index,5])-(part_real.iloc[index,3]))/abs((part_real.iloc[index,3])+(part_forecasted.iloc[index,5]))
    counter+=1
    
print('Temperature mean percentage error: ',"%.4f" % round(error/counter, 4))
print('Pressure mean percentage error: ',"%.4f" % round(error_1/counter, 4))
print('Wind speed mean percentage error: ',"%.4f" % round(error_2/counter, 4))
print('precipitation mean percentage error: ',"%.4f" % round(error_3/counter, 4))


print('Simulation Temperature STD: ',"%.4f" % round(statistics.stdev(part_forecasted.iloc[:,0]), 4))
print('Simulation Temperature STD: ',"%.4f" % round(statistics.stdev(part_real.iloc[:,0]), 4))
#print('Pressure mean percentage error: ',"%.4f" % round(statistics.stdev(sample), 4))
####################################################################### corrlation

corr_temperature=part_forecasted['Temperature[Degree Celsius]'].corr(part_real['Temp (¡ãC)'])
corr_pressure=(part_forecasted['Surface Pressure [Pa]']).corr(part_real['Stn Press (kPa)']*1000)
#corr_wind=part_forecasted['Wind[km/h]'].corr(part_real['Wind Spd (km/h)'])
#corr_precipitation=part_forecasted['precipitation[mm]'].corr(part_real['Precip. Amount (mm)'])
#corr_humidity=part_forecasted['relative humidity'].corr(part_real['Rel Hum (%)'])
#corr_irradiance=part_forecasted['irradiance'].corr(part_new['irradiance'])
#
print('Temperature Correlation is: ',corr_temperature)
print('Pressure Correlation is: ',corr_pressure)
#print('Wind speed Correlation is: ',corr_wind)
#print('Precipitation Correlation is: ',corr_precipitation)
#print('Relative humidity Correlation is: ',corr_humidity)
#print('Irradiance Correlation is: ',corr_irradiance)

#plt.figure(figsize=(12,12))
#part_real_corr_matrix=part_real.corr()
#
#plt.matshow(part_real_corr_matrix,fignum=1)
#name=['Temp (Â°C)','Stn Press (kPa)','Wind Spd (km/h)','Precip. Amount (mm)']
#
#name_pos=np.arange(len(name))
#
#plt.xticks(name_pos,name)
#plt.yticks(name_pos,name)
#plt.colorbar()
#########################################################################################
#a=part_forecasted.iloc[:,1]
#b=part_real.iloc[:,1]*1000
#
#def dtw_cost(ts1,ts2):
#    len_1=len(ts1)
#    len_2=len(ts2)
#    matrix=np.zeros((len_1,len_2))#length ts1 rows, length ts2 columes
#    for i in range(len_1):
#        for j in range(len_2):
#            matrix[i,j]=np.inf
#    for i2 in range(len_1):
#        for j2 in range(len_2):
#            if(i2 != 0 and j2 != 0):
#                matrix[i2,j2]=np.sqrt((ts1[i2]-ts2[j2])**2)+np.min([matrix[i2-1,j2],matrix[i2,j2-1],matrix[i2-1,j2-1]])
#            elif i2 == 0 and j2 != 0:
#                matrix[i2,j2]=np.sqrt((ts1[i2]-ts2[j2])**2)+matrix[i2,j2-1]
#            elif i2 != 0 and j2 == 0:
#                matrix[i2,j2]=np.sqrt((ts1[i2]-ts2[j2])**2)+matrix[i2-1,j2]
#            elif i2 == 0 and j2 == 0:
#                matrix[i2,j2]=np.sqrt((ts1[i2]-ts2[j2])**2)
#    return matrix
#    
#    
#def dtw_distance(cost_matrix):
#    d=[]
#    path=[]
#    row_index=len(cost_matrix)-1
#    col_index=len(cost_matrix[0])-1
#    d.append(cost_matrix[row_index,col_index])
#    path.append([row_index,col_index])
#    while row_index!=0 or col_index!=0:
#        if row_index>0 and col_index>0:
#            if cost_matrix[row_index-1,col_index]<cost_matrix[row_index,col_index-1] and cost_matrix[row_index-1,col_index]<cost_matrix[row_index-1,col_index-1]:
#                d.append(cost_matrix[row_index-1,col_index])
#                row_index=row_index-1
#                path.append([row_index,col_index])
#            elif cost_matrix[row_index,col_index-1]<=cost_matrix[row_index-1,col_index] and cost_matrix[row_index,col_index-1]<cost_matrix[row_index-1,col_index-1]: 
#                d.append(cost_matrix[row_index,col_index-1])
#                col_index=col_index-1
#                path.append([row_index,col_index])
#            elif cost_matrix[row_index-1,col_index-1]<=cost_matrix[row_index-1,col_index] and cost_matrix[row_index-1,col_index-1]<=cost_matrix[row_index,col_index-1]: 
#                d.append(cost_matrix[row_index-1,col_index-1])
#                col_index=col_index-1
#                row_index=row_index-1
#                path.append([row_index,col_index])
#        elif row_index==0 and col_index>0:
#            d.append(cost_matrix[row_index,col_index-1])
#            col_index=col_index-1
#            path.append([row_index,col_index])
#        elif row_index>0 and col_index==0:
#            d.append(cost_matrix[row_index-1,col_index])
#            row_index=row_index-1
#            path.append([row_index,col_index])
#            
#    print('The DTW distance is: ',round(np.sum(d)/len(d),4))
##    print(path)
##    print(d)
#    return path
#
#def dtw_path(pair,d1,d2):
#    re_d1=[]
#    re_d2=[]
#    index=len(pair)
#    for i in range(index):
#        re_d1.append(a[pair[i][0]])
#        re_d2.append(b[pair[i][1]])
#    re_d1.reverse()
#    re_d2.reverse()
#    return re_d1,re_d2
#        
#        
#    
#
#c_matrix=dtw_cost(a,b)
#path_pair=dtw_distance(c_matrix)
#warping_d1,warping_d2=dtw_path(path_pair,a,b)
#
#path_x = [p[1] for p in path_pair]
#path_y = [p[0] for p in path_pair]
#
#path_xx = [x+0.5 for x in path_x]
#path_yy = [y+0.5 for y in path_y]
#
#fig, ax = plt.subplots(figsize=(12, 12))
#ax = sns.heatmap(c_matrix, cmap="YlGnBu",square=True, linewidths=0.1,ax=ax)
#bottom, top = ax.get_ylim()
#ax.set_ylim(bottom + 0.5, top - 0.5)
#ax.invert_yaxis()
#
#ax.plot(path_xx, path_yy, color='red', linewidth=3, alpha=0.5)
#
#plt.figure(figsize=(12,12))
#plt.plot(a.index,a,color='b',label='date set 1')
#plt.plot(b.index,b,color='r',label='date set 2')
#plt.title('Energy Data Plot')
#plt.xlabel('Index')
#plt.ylabel('Normalized')
#plt.legend(loc="upper left")
#
#for i in range(len(path_pair)):
#    x1=path_pair[i][0]
#    x2=path_pair[i][1]
#    y1=a[x1]
#    y2=b[x2]
#    temp=[[x1,x2],[y1,y2]]
#    plt.scatter(temp[0],temp[1],marker='o',color='k');
#    plt.plot(temp[0],temp[1],'--',color='k',alpha=0.3)
#    
#plt.show()  
#
#plt.figure(figsize=(12,12))
#plt.plot(warping_d1,color='b',label='adjusted path date set 1')
#plt.plot(warping_d2,color='r',label='adjusted path date set 2')
#plt.title('Energy adjusted Data Plot')
#plt.xlabel('Index')
#plt.ylabel('Normalized')
#plt.legend(loc="upper left")
#
#corr_wind_new=np.corrcoef(warping_d1,warping_d2)[1,0]
#print('DTW Wind speed Correlation is: ',corr_wind_new)

