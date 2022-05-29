# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 13:01:22 2021

@author: levan
"""

# Description:

# This script can take a txt file from jatos, that contains multiple 
# participant data, and break it up into txt files for each individual 
# participant, and save them.


# Import other libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import json

# %% Global setup

print(os.getcwd())

# Set the working directory
os.chdir('../../')

saveData       = True

# %% Import the pid mappings

if os.getenv('COMPUTERNAME') == 'DESKTOP-CILGRCL':
    pid_mapping = pd.read_excel('C:\\Users\\levan\\Desktop\\density_pid_map.xlsx')
else:
    pid_mapping = pd.read_excel('C:\\Users\\lb08\\Desktop\\density_pid_map.xlsx')


# %% Import the files

file_name = 'jatos_results_batch1.txt'

f = open('./data/pilots/gui_downloads/' + file_name,'r')    

rawtext = f.read()

rawtext_split = rawtext.splitlines()

# %% How many prolific ID components do we have?
pid_counter = 0
pid_idxs = []
for idx, iLine in enumerate(rawtext_split):
    if iLine.find('[get_pid_comp_start---') !=-1:
        pid_counter += 1
        pid_idxs.append(idx)

# %% Look to split the file and save individual txt files
    
# Loop over all get_pid_component start positions.
for iP in range(0,len(pid_idxs)):
    print(iP)
    
    # Get the component before iP
    iIdx_start = pid_idxs[iP]
    
    # If its the last 'get_pid' component, the next one doesn't exist so, the 
    # iIdx_end has to be the length of rawtext_split
    if iP == len(pid_idxs)-1:
        iIdx_end = len(rawtext_split) + 1
    else:
        iIdx_end = pid_idxs[iP+1]
    
    # Join all these componenets
    tosave = '\n'.join(rawtext_split[iIdx_start:iIdx_end])
    
    # Whats the prolific ID
    json_start_loc = rawtext_split[iIdx_start].find('[get_pid_comp_start---') + \
        len('[get_pid_comp_start---')
    json_end_loc = rawtext_split[iIdx_start].find('---get_pid_comp_end')
    json_text = rawtext_split[iIdx_start][json_start_loc:json_end_loc]    
    iData_decoded = json.loads(json_text)
    if 'prolific_ID' in iData_decoded:
        iPID = iData_decoded['prolific_ID']
    elif 'prolific_ID' in iData_decoded['inputData']:
        iPID = iData_decoded['inputData']['prolific_ID']
    
    # Whats the anonimized ID?
    anonID = pid_mapping.studyID[pid_mapping.prolificID == iPID].iloc[0]
    
    # Find the prolific ID in the tosave file and substitute
    tosave = tosave.replace(iPID,anonID)
    
    if saveData:
        # Save this data
        f= open('./data/pilots/gui_downloads/jatos_prolific_id_' + anonID + '.txt',"w+")    
        
        f.write(tosave)
        f.close()