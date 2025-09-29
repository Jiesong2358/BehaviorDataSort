# this script is used to calculate the onset and duration
# write them to the existed tsv file, which included the definde trial_type
# By Haozhe & Jie, 2023/10/16
import pandas as pd
import numpy as np
import glob
import os
# Input directory for CSV files: sub-*_task-*_run-*_timeline.csv
data_dir = 'S:/GVuilleumier/GVuilleumier/groups/jies/Spatial_Navigation/Pilots_Data/Data_Raw/timeline/all_new'
output_dir = 'C:/Jie_Documents/Navigation/Outputs/Events_Files/Intersection_Modulation/1'
file_lists = glob.glob(f"{data_dir}/*/*retra*.csv")
for file_path in file_lists:
    # Extract the file name and sub-folder from the file path
    glob_file = file_path.split('/')[-1]
    csv_file = glob_file.split('\\')[-1]
    sub_folder = glob_file.split('\\')[-2]
    # Create output directory if it doesn't exist
    os.makedirs(f"{output_dir}/{sub_folder}", exist_ok=True)
    # Initialize a dictionary to store event data
    data_dict = {'TimeStamp': [], 'EventID': [], 'Event': []}
    # Read the CSV file and populate the data dictionary
    with open(file_path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if i == 0:
                continue
            line_list = line.strip().split(',')
            data_dict['TimeStamp'].append(float(line_list[0]))
            data_dict['EventID'].append(line_list[1])
            data_dict['Event'].append(line_list[2])
    # Calculate the Response time for each trial
    duration_df = pd.DataFrame(data_dict)
    filtered_pd1 = duration_df[duration_df['Event'].isin(['Ret_Intersection_Stop', 'Ret_Response', '#ROUTE'])]
    timestamps = filtered_pd1['TimeStamp'].values
    events1 = filtered_pd1['Event'].values
    ROUTE_index = np.where(np.logical_and(events1 != '#ROUTE', events1 != 'Ret_Response'))[0]
    response_time = np.array((timestamps[1:] - timestamps[:-1]) / 1000)[ROUTE_index]
    remove_words = 'Timeline'
    file_name = csv_file.split('.')[0][:-len(remove_words)] + 'modulation.tsv'
    output_file = f"{output_dir}/{sub_folder}/{file_name}"
    existing_df = pd.read_csv(output_file, sep='\t')
    existing_df['modulation'] = 0    
    i0_mask = existing_df['trial_type'].str.contains('_I0')
    # Fill response times for non-'*_I0' trials
    existing_df.loc[~i0_mask, 'modulation'] = response_time
    # Fill 0 for '*_I0' trials
    existing_df.loc[i0_mask, 'modulation'] = 0
    existing_df.to_csv(output_file, sep='\t', index=False)




