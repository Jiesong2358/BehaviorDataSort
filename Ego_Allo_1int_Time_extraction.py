import pandas as pd
import numpy as np
import glob
import os
import re
import shutil

# Step 1: Find and filter the CSV files
base_dir = 'S:/GSani/JieSong/1.Data/raw_data/1Intersection'
in_dir = f'{base_dir}/*/merged_timeline'
in_files = glob.glob(f"{in_dir}/sub-*_task-dir_rep1_run-*_Timeline.csv")
trial_type_file = glob.glob(f"{base_dir}/conditions/merged_Jie/int1_Run*.xlsx")
# trial_type_response = glob.glob(f"{base_dir}/conditions/Response/RepRet_Run*.xlsx")

# Step 2: Define a function to merge and save files for each run
for file_path in in_files:
    # Extract the run number from the CSV file name
    run_number = re.search(r'_run-(\d+)_', file_path).group(1)
    # Find the corresponding trial_type_imagination file for this run
    matching_trial_type_imag = [f for f in trial_type_file if f.endswith(f"int1_Run{run_number}.xlsx")]
    if not matching_trial_type_imag:
        print(f"No matching trial_type file found for Run {run_number}")
        continue
    trial_type_file_imag = matching_trial_type_imag[0]
    
    sub_name = file_path.split('\\')[-3]
    glob_file = file_path.split('/')[-1]
    csv_file = glob_file.split('\\')[-1]
    out_dir = f"{base_dir}/{sub_name}/events_files"
    os.makedirs(out_dir, exist_ok=True) 
    data_dict = {'TimeStamp':[], 'EventID':[], 'Event':[]}
    duration_df1 =pd.read_csv(file_path)
    with open(file_path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            line_list = line.strip().split(',')
            data_dict['TimeStamp'].append(float(line_list[0]))
            data_dict['EventID'].append(line_list[1])
            data_dict['Event'].append(line_list[2])

# step 3: Calculate the duration & onset of retrieval for each trial      
    onset_df = pd.DataFrame(data_dict)
    # Identify start and stop events within each trial (paired by '#ROUTE')
    sync_time = onset_df[onset_df['Event'] == '[MRI_Sync]']['TimeStamp'].values[0]
    trial_starts_times = onset_df[(onset_df['Event'] == 'Rep1_IntersectionStop') | 
                                  (onset_df['Event'] == 'Dir_Intersection_Stop')]['TimeStamp'].values
    trial_stop_times = onset_df[(onset_df['Event'] == 'Rep1_Response') | 
                               (onset_df['Event'] == 'Dir_Response')]['TimeStamp'].values
    # Calculate the duration of imagination for each trial
    onset = (trial_starts_times - sync_time) / 1000
    duration = [2 if 'Rep1' in event else 4 for event in onset_df[(onset_df['Event'] == 'Rep1_IntersectionStop') | (onset_df['Event'] == 'Dir_Intersection_Stop')]['Event'].values]
    # trial_type with land mark positions;
    # trial_types = pd.read_excel(trial_type_file_imag)['trial_type'].values
    # trial_types = [f"retrieval_{tt}" for tt in trial_types] trial_type_df = pd.read_excel(trial_type_file_imag)
    # trial_type without land mark positions;
    trial_type_df = pd.read_excel(trial_type_file_imag)
    trial_type_df['trial_type'] = trial_type_df['trial_type'].str.extract(r'^(ego|allo)')
    trial_type_df = trial_type_df.dropna(subset=['trial_type'])
    trial_types = [f"retrieval_{tt}" for tt in trial_type_df['trial_type'].values]
    response_time = (trial_stop_times - trial_starts_times) / 1000
    # define the imagination file name
    remove_words = 'Timeline'
    file_name = csv_file.split(remove_words)[0] + 'ego_allo.tsv'
    output_file_path = f"{out_dir}/{file_name}"
    output_df = pd.DataFrame({
        'onset': onset,
        'duration': duration,
        'trial_type': trial_types,
        # 'trial_type': pd.read_excel(trial_type_file_imag)['trial_type'].values
        'response_time': response_time
        })
    output_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Retrieval dataframe saved to: {output_file_path}")
# step 4: Calculate the duration & onset of encoding for each trial   
    encoding_start_time = onset_df[(onset_df['Event'] == 'Rep1_Encoding_Start') | 
                                (onset_df['Event'] == 'Dir_Encoding_Start')]['TimeStamp'].values

    encoding_onset = (encoding_start_time - sync_time) / 1000
    encoding_duration = 4
    encoding_trial_types = [f"encoding_{tt}" for tt in trial_type_df['trial_type'].values]
    file_name = csv_file.split(remove_words)[0] + 'ego_allo_encoding.tsv'
    output_file_path = f"{out_dir}/{file_name}"
    output_df = pd.DataFrame({
        'onset': encoding_onset,
        'duration': encoding_duration,
        'trial_type': encoding_trial_types,
        })
    output_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Encoding dataframe saved to: {output_file_path}")
    
import shutil
import glob
import os

base_dir = 'S:/GSani/JieSong/1.Data/raw_data/1Intersection'
#step n: copy the events files to the new directory
dest_base_dir = r"S:/GVuilleumier/GVuilleumier/groups/jies/Spatial_Navigation/Final_data/nifti_new"
source_files = glob.glob(f"{base_dir}/sub*/events_files/*.tsv")

for src_file in source_files:
    # Extract the sub-folder name from the source path
    sub_folder = re.search(r"sub-\d+", src_file).group(0) 
    # Define the corresponding destination folder
    dest_folder = os.path.join(dest_base_dir, sub_folder, "func")
    os.makedirs(dest_folder, exist_ok=True)  # Create the destination folder if it doesn't exist
    # Copy the file to the destination
    shutil.copy(src_file, dest_folder)
    print(f"Copied {src_file} to {dest_folder}")