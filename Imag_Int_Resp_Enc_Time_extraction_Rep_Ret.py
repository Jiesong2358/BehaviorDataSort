import pandas as pd
import numpy as np
import glob
import os
import re
import shutil

# Step 1: Find and filter the CSV files
base_dir = 'S:/GSani/JieSong/1.Data/raw_data'
in_dir = f'{base_dir}/*/merged_timeline'
in_files = glob.glob(f"{in_dir}/sub-*_task-rep_ret_run-*_Timeline.csv")
trial_type_imagination = glob.glob(f"{base_dir}/conditions/Imagination/RepRet_Run*.xlsx")
trial_type_response = glob.glob(f"{base_dir}/conditions/Response/RepRet_Run*.xlsx")

# Step 2: Define a function to merge and save files for each run
for file_path in in_files:
    # Extract the run number from the CSV file name
    run_number = re.search(r'_run-(\d+)_', file_path).group(1)
    # Find the corresponding trial_type_imagination file for this run
    matching_trial_type_imag = [f for f in trial_type_imagination if f.endswith(f"RepRet_Run{run_number}.xlsx")]
    if not matching_trial_type_imag:
        print(f"No matching trial_type_imagination file found for Run {run_number}")
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

# step 3: Calculate the duration & onset of imagination for each trial      
    duration_df = pd.DataFrame(data_dict)
    # Identify start and stop events within each trial (paired by '#ROUTE')
    sync_time = duration_df[duration_df['Event'] == '[MRI_Sync]']['TimeStamp'].values[0]
    trial_starts_times = duration_df[(duration_df['Event'] == 'Rep_Imagination_Start') | (duration_df['Event'] == 'Ret_Imagination_Start')]['TimeStamp'].values
    trial_stops_times = duration_df[(duration_df['Event'] == 'Rep_Imagination_Stop') | (duration_df['Event'] == 'Ret_Imagination_Stop')]['TimeStamp'].values

    # Calculate the duration of imagination for each trial
    onset = (trial_starts_times - sync_time) / 1000
    duration = (trial_stops_times - trial_starts_times) / 1000
    # define the imagination file name
    remove_words = 'Timeline'
    file_name = csv_file.split(remove_words)[0] + 'imagination.tsv'
    output_file_path = f"{out_dir}/{file_name}"
    output_df = pd.DataFrame({
        'onset': onset,
        'duration': duration,
        'trial_type': pd.read_excel(trial_type_file_imag)['trial_type'].values
    })
    output_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Imagination dataframe saved to: {output_file_path}")

# Step 4: Calculate the duration & onset of response for each trial
    matching_trial_type_resp = [f for f in trial_type_response if f.endswith(f"RepRet_Run{run_number}.xlsx")]
    if not matching_trial_type_resp:
        print(f"No matching trial_type_response file found for Run {run_number}")
        continue
    trial_type_file_resp = matching_trial_type_resp[0]

    response_indexes = duration_df[(duration_df['Event'] == 'Rep_Response') | (duration_df['Event'] == 'Ret_Response')].index
    pre_response_times = duration_df.loc[response_indexes - 1, 'TimeStamp'].values
    after_response_times = duration_df.loc[response_indexes + 1, 'TimeStamp'].values
    # Calculate the duration of response for each trial
    onset_response = (pre_response_times - sync_time) / 1000
    duration_response = (after_response_times - pre_response_times) / 1000
    # define the response file name
    remove_words = 'Timeline'
    response_file_name = csv_file.split(remove_words)[0] + 'response.tsv'
    output_response_path = f"{out_dir}/{response_file_name}"
    out_response_df = pd.DataFrame({
        'onset': onset_response,
        'duration': duration_response,
        'trial_type': pd.read_excel(trial_type_file_resp)['trial_type'].values
    })
    out_response_df.to_csv(output_response_path, sep='\t', index=False)
    print(f"Response dataframe saved to: {output_response_path}")
# Step 5: Calculate the duration & onset of encoding for each trial
    matching_trial_type_resp = [f for f in trial_type_response if f.endswith(f"RepRet_Run{run_number}.xlsx")]
    if not matching_trial_type_resp:
        print(f"No matching trial_type_response file found for Run {run_number}")
        continue
    trial_type_file_resp = matching_trial_type_resp[0]
    
    # Define encoding intersection events and stop events
    rep_encoding_events = ['Rep_Encoding_Intersection_Stop']
    ret_encoding_events = ['Ret_Encoding_Intersection_Stop']
    rep_stop_event = 'Rep_Encoding_Stop'
    ret_stop_event = 'Ret_Encoding_Stop'

    # Extract only relevant encoding events
    encoding_df = duration_df[duration_df['Event'].isin(rep_encoding_events + ret_encoding_events + [rep_stop_event, ret_stop_event])].copy()
    encoding_df = encoding_df.sort_values(by='TimeStamp').reset_index(drop=True)
    onset_list, duration_list, trial_type_list = [], [], []
    def process_encoding_events(event_list, stop_event, prefix):
        timestamps = []  # Store timestamps for int1, int2, int3, stop
        for _, row in encoding_df.iterrows():
            event = row['Event']
            timestamp = row['TimeStamp']
            if event in event_list:
                timestamps.append(timestamp)  # Collect timestamps for int1, int2, int3 
            if event == stop_event and len(timestamps) == 3:
                timestamps.append(timestamp)  # Stop event marks the end
                for i in range(3):
                    onset_list.append((timestamps[i] - sync_time) / 1000)
                    duration_list.append((timestamps[i + 1] - timestamps[i]) / 1000)
                    trial_type_list.append(f"{prefix}_int{i + 1}")
                
                timestamps = []  # Reset for next block
    process_encoding_events(rep_encoding_events, rep_stop_event, "rep_encoding")
    process_encoding_events(ret_encoding_events, ret_stop_event, "ret_encoding")
    final_encoding_df = pd.DataFrame({
        'onset': onset_list,
        'duration': duration_list,
        'trial_type': trial_type_list
    })
    encoding_file_name = csv_file.split('Timeline')[0] + 'encoding.tsv'
    output_encoding_path = f"{out_dir}/{encoding_file_name}"
    final_encoding_df.to_csv(output_encoding_path, sep='\t', index=False)
    print(f"Encoding dataframe saved to: {output_encoding_path}")

# Step 5: copy imagination.tsv and response.tsv 
# from S:\GSani\JieSong\1.Data\raw_data\sub*\events_files\ 
# to S:\GVuilleumier\GVuilleumier\groups\jies\Spatial_Navigation\Final_data\nifti_new\sub*\func
dest_base_dir = r"S:/GVuilleumier/GVuilleumier/groups/jies/Spatial_Navigation/Final_data/nifti_new"
# Find all imagination.tsv and response.tsv files in the source directories
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