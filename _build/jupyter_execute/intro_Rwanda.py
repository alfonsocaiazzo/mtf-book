#!/usr/bin/env python
# coding: utf-8

# # The Multi-tier framework for measuring energy access
# 
# This section analized the energy access data published by the 
# [ESMAP Sector of the World Bank](https://mtfenergyaccess.esmap.org/country/rwanda), related to the energy access assessment in Rwanda. 
# 
# The assessment is based on the [Multi-Tier Framework]() (see the table bellow). In this approach, energy access is evaluated across a range of dimensions (called *attributes*). Along each attribute, each household is ranked in a 
# **tier** (a level), from 0 (no access to energy) to 5 (full access to energy). The final energy access ranking
# is then defined as the **minimum** over all attributed.
# 
# The report concerning the study in Rwanda can be downloaded [here](https://energydata.info/dataset/rwanda-multi-tier-framework-mtf-survey-2018). This report details the results of the MTF survey implemented in Rwanda's five provinces in 2016 and was published in 2018. It provides results about both access to electricity and access to modern energy cooking solutions in the country. 
# 
# In this section, we compare our own data analysis to this MTF report, starting from the same database. 
# 

# In[1]:


from IPython.display import Image


# In[2]:


Image('../Rwanda/references/MTF_energy_access.png')

