#!/usr/bin/env python
# coding: utf-8

# # Household Energy Access Assessment in DRC
# 
# The objective of this project is to analyze access to energy (electricity and cooking solution) in rural areas of the Democratic Republic of Congo. 
# 
# The study has been implemented by APIDE, a local NGO working in the regions of Kitutu, Kaituga, and Mwenga, in the eastern part of the country, about 150 km from the border with Burundi and Rwanda.
# 
# Data collection, processing, and visualization have been supported by the [HEDERA Impact Toolkit](https://hit.hedera.online)
# This digital report has been created as a [jupyter-book](https://jupyterbook.org/intro).
# 
# Relevant information concerning the use, associated costs, and various attributes of access to electricity and cooking solutions has been collected from households APIDE is working with in rural and remote areas, using the HEDERA collect mobile app based on the [OpenDataKit](https://opendatakit.org) open-source framework. 
# The HEDERA Impact Toolkit allows institutions to efficiently establish a baseline for monitoring progress towards the Sustainable Development Goals (SDGs) and track the progress thereof, following, for example, the [Multi-tier Framework](https://www.esmap.org/node/55526) (MTF) for SDG7, recently established by The World Bank, and the Progress out of Energy Poverty Index (PEPI) [N. Realpe, PhD Thesis 2017](https://depositonce.tu-berlin.de/handle/11303/6708).
# 
# 
# ## Methodology
# 
# HEDERA provided a mobile application for data collection, as well as digital material for remote training.
# Members of APIDE field staff were trained during a one-day workshop (held by one member of the organization).
# During 10 days, more than 220 data point were collected (household rosters, electricity assessment, cooking solution assessment).
# 
# You can also visit the [full report](https://hedera-platform.github.io/report-apide/summary.html) of this case study.
# 

# In[1]:


HIT_PATH = '../../../HIT/src/'
institution_id = 7
lang = 'en'
import os,sys, folium
sys.path.insert(0, os.path.normpath(os.path.join(os.path.abspath(''), HIT_PATH)))
import hedera_types as hedera
import odk_interface as odk

mfi = hedera.mfi(institution_id,setPathBook=True)
mfi.odk_data_name = "../../../ODK_Collect_Data/Apide/Data/SDG7/results.csv"
data = mfi.read_survey(mfi.odk_data_name)
mfi.HH = odk.households(data)


# ## Collection overview
# 
# ### Map
# The Map allows to visualize the location of the collected GPS data. Missing data points are displayed with coordinated *(0,0)*

# In[2]:


import matplotlib.pyplot as plt

select = mfi.HH['GPS_Latitude']!=0
HH_with_GPS = mfi.HH[select]

# change plot layout
plt.rcParams.update({'font.size': 20})
#Define initial geolocation
lat_center = HH_with_GPS['GPS_Latitude'].mean() 
lon_center = HH_with_GPS['GPS_Longitude'].mean()
max_var = max(HH_with_GPS['GPS_Latitude'].var(),HH_with_GPS['GPS_Longitude'].var())
zoom_start = 9
if max_var>0.1:
    zoom_start -= 1
if max_var>1:
    zoom_start -= 1
initial_location = [lat_center, lon_center]

# create map
map_osm = folium.Map(initial_location, zoom_start=zoom_start)
colors = {0: hedera.tier_color(0), 1 : hedera.tier_color(1), 2 : hedera.tier_color(2), 
          3 : hedera.tier_color(3), 4 : hedera.tier_color(4), 5: hedera.tier_color(5)}
HH_with_GPS.apply(lambda row:folium.CircleMarker(location=[row["GPS_Latitude"], row["GPS_Longitude"]],
                                        radius=10,fill_color="#FF5733",popup=(row["GPS_Latitude"],row["GPS_Longitude"],row["locality"])).add_to(map_osm), axis=1)
map_osm


# ### Data per location
# Data have been collected in three different areas in Eastern DRC.

# In[3]:


import matplotlib.pyplot as plt
# this is needed if the surveys do not cover all states/offices
empty = []
for o in mfi.offices:
    select = mfi.HH['locality']==o
    
    if sum(select)==0:
        empty.append(o)
        
for o in empty:
    mfi.offices.remove(o)
        
mfi.plot_collection_barh()


# ## Dates of Collection
# The following figure shows the amount of surveys per day

# In[4]:


import numpy as np
S = odk.get_survey_duration(data)
dates = np.unique(np.array(mfi.HH['date']))
ind = np.arange(len(dates))
dates_plot = []
dates_labels = []

mean_e = []
mean_c = []
mean_tot = []

for d in dates:
    
    select = mfi.HH['date']== d
    dates_plot.append( sum(select) )
    dates_labels.append(d)
    
    # get surveys data on a diven date
    surveys = S[select]    
    
    selectE = surveys['electricity']>0
    surveysE = surveys[selectE]
    mean_e.append(surveysE['electricity'].mean())
    
    selectC = surveys['cooking']>0
    surveysC = surveys[selectC]
    mean_c.append(surveysC['cooking'].mean())
    
    selectT = surveys['total']>0
    surveysT = surveys[selectT]
    mean_tot.append(surveys['total'].mean())
    import matplotlib.pyplot as plt

# change plot layout
plt.rcParams.update({'font.size': 20})
# survey per date    
fig, ax = plt.subplots(figsize=(10,8))      
plt.bar(ind, dates_plot, width=0.95,edgecolor='white')
plt.xticks(ind, dates, rotation=90)
ax.yaxis.grid(color='grey', linestyle='--', linewidth=0.5)
plt.show()


# ### Average Duration
# Average survey duration per day was on average between 5 and 27 minutes.
# 
# **Note**: Some interviews only covered the household roster and are therefore much shorter.

# In[5]:


import matplotlib.pyplot as plt

# change plot layout
plt.rcParams.update({'font.size': 20})
# survey duration
fig, ax = plt.subplots(figsize=(10,8))      
plt.bar(ind, mean_tot, width=0.95,edgecolor='white',color='blue',label='Total')
plt.xticks(ind, dates, rotation=90)
plt.legend(framealpha=1,frameon=False,bbox_to_anchor=(1.25,1.0),
                       loc='upper center').set_draggable(True)
ax.yaxis.grid(color='grey', linestyle='--', linewidth=0.85) # vertical lines
plt.show()


# ## Electricity Access Attributes 
# 

# In[6]:


import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
mfi.tier_barh(hedera.keys().attributes_electricity[0:8],
              hedera.names('en').e_attributes[0:8],legend=True)


# ## Primary Electricity Sources

# In[7]:


import matplotlib.pyplot as plt
mfi.electricity_sources_summary(lang='en',legend=True)


# ## Household Appliances

# In[8]:


import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
[appliances_per_x,u_id] = odk.compute_appliances_per_x(data,mfi.HH,mfi.offices,'locality')
odk.plot_appliances_per_x(len(mfi.HH),appliances_per_x,u_id,'locality',
                          mfi.offices,
                          figPath=None,c=mfi.office_color,lang=lang)


# ## MTF Electricity Index vs. Primary Source

# In[9]:


import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
mfi.stacked_tier_per_category('E_Index',hedera.keys().powerSources,
                              'primary_electricity_source',
                              hedera.names('en').powerSources,legend=True)


# ## Access to Modern Cooking Solutions Attributes
# 

# In[10]:


import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
mfi.tier_barh(hedera.keys().attributes_cooking[0:4],hedera.names('en').c_attributes[0:4],legend=True)


# ### Primary Cooking Stoves

# In[11]:


import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
mfi.cooking_fuels_summary(lang='en',legend=True)


# ### MTF Index (Access to Cooking Solutions) vs. Primary Cooking Fuel

# In[12]:


import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
mfi.stacked_tier_per_category('C_Index',hedera.keys().fuels,
                              'primary_cooking_fuel',
                              hedera.names('en').fuels)

