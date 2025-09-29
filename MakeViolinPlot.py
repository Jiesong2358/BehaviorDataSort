# # import pandas as pd
# # import numpy as np
# # import glob
# # import os
# # import re

# # # Step 1: Find and filter the CSV files
# # base_dir = 'S:/GSani/JieSong/1.Data/raw_data'
# # in_dir = f'{base_dir}/*/merged_timeline'
# # in_files = glob.glob(f"{in_dir}/sub-*_task-rep_ret_run-*_Timeline.csv")
# # trial_type_response = glob.glob(f"{base_dir}/conditions/Response/*.csv")

# # # Step 2: Define a function to merge and save files for each run
# # for file_path in in_files:
# #     # Extract the run number from the CSV file name
# #     run_number = re.search(r'_run-(\d+)_', file_path).group(1)
# #     matching_trial_type_resp = [f for f in trial_type_response if f.endswith(f"Run{run_number}.csv")]
# #     if not matching_trial_type_resp:
# #         print(f"No matching trial_type_response file found for Run {run_number}")
# #         continue
# #     trial_type_file_resp = matching_trial_type_resp[0]
    
# #     sub_name = file_path.split('\\')[-3]
# #     glob_file = file_path.split('/')[-1]
# #     csv_file = glob_file.split('\\')[-1]
# #     out_dir = f"{base_dir}/{sub_name}/events_files"
# #     os.makedirs(out_dir, exist_ok=True) 
# #     data_dict = {'TimeStamp':[], 'EventID':[], 'Event':[]}
# #     duration_df1 =pd.read_csv(file_path)
# #     with open(file_path, 'r') as f:
# #         for i, line in enumerate(f.readlines()):
# #             line_list = line.strip().split(',')
# #             data_dict['TimeStamp'].append(float(line_list[0]))
# #             data_dict['EventID'].append(line_list[1])
# #             data_dict['Event'].append(line_list[2])

# #     # step 3: Calculate the duration & onset of imagination for each trial      
# #     duration_df = pd.DataFrame(data_dict)
# #     # Identify start and stop events within each trial (paired by '#ROUTE')
# #     sync_time = duration_df[duration_df['Event'] == '[MRI_Sync]']['TimeStamp'].values[0]

# #     # Step 4: Calculate the duration & onset of response for each trial
# #     response_indexes = duration_df[(duration_df['Event'] == 'Rep_Response') | (duration_df['Event'] == 'Ret_Response')].index
# #     pre_response_times = duration_df.loc[response_indexes - 1, 'TimeStamp'].values
# #     after_response_times = duration_df.loc[response_indexes + 1, 'TimeStamp'].values
# #     # Calculate the duration of response for each trial
# #     onset_response = (pre_response_times - sync_time) / 1000
# #     duration_response = (after_response_times - pre_response_times) / 1000
# #     # define the response file name
# #     remove_words = 'Timeline'
# #     response_file_name = csv_file.split(remove_words)[0] + 'response.tsv'
# #     output_response_path = f"{out_dir}/{response_file_name}"
# #     out_response_df = pd.DataFrame({
# #         'onset': onset_response,
# #         'duration': duration_response,
# #         'trial_type': pd.read_csv(trial_type_file_resp)['trial_type'].values
# #     })
# #     out_response_df.to_csv(output_response_path, sep='\t', index=False)
# #     print(f"Response dataframe saved to: {output_response_path}")
# # aa=1

# # Step03: plot the merged behavior data for repetition and retracing for all subjects
# # Save the plots to the "figures" folder
# # only plot the correct trials
# import os
# import matplotlib.pyplot as plt
# import pandas as pd

# base_dir = 'S:/GSani/JieSong/1.Data/raw_data'
# figure_path = os.path.join(base_dir, 'figures')
# aver_path = os.path.join(base_dir, 'figures', 'aver_rt_acc')

# # Iterate over each subject directory
# for subject_dir in os.listdir(base_dir):
#     if not subject_dir.startswith('sub'):
#         continue
#     input_dir = os.path.join(base_dir, subject_dir, 'condition_behavior')
#     out_dir = os.path.join(base_dir, subject_dir, 'merged_behavior')
    
#     if not os.path.exists(figure_path):
#         os.makedirs(figure_path)
        
#     if not os.path.exists(out_dir):
#         os.makedirs(out_dir)
        
#     csv_files = [file for file in os.listdir(input_dir) if file.endswith('.csv')]
#     #### Plot all sujects behavior data for repetition and retracing
#     # csv_files = [file for file in os.listdir(out_dir) if file.endswith('aver_rt.csv')]
#     repe_data = pd.DataFrame()
#     retra_data = pd.DataFrame()

#     for csv_file in csv_files:
#         csv_path = os.path.join(input_dir, csv_file)
#         data = pd.read_csv(csv_path)
#         if len(data.columns) == 1:
#             data = pd.read_csv(csv_path, sep=';')
#         data.columns = data.columns.str.strip()

#         # Check if 'accuracy' column exists
#         if 'accuracy' in data.columns:
#             # Check if all accuracy values are 1
#             if (data['accuracy'] == 1).all():
#                 num_remaining_blocks = data['block'].nunique()
#             else:
#                 blocks_with_zero_accuracy = data[data['accuracy'] == 0]['block'].unique()
#                 data = data[~data['block'].isin(blocks_with_zero_accuracy)]
#                 num_remaining_blocks = data['block'].nunique()
#         else:
#             print("Accuracy column not found in the DataFrame.")
        
#         # Write the number of remaining blocks to a text file
#         txt_file_path = os.path.join(out_dir, f'{os.path.splitext(csv_file)[0]}_remaining_blocks.txt')
#         with open(txt_file_path, 'w') as txt_file:
#             txt_file.write(f"Remaining Blocks: {num_remaining_blocks}")
        

#         # Group the data for further processing
#         grouped_data = data.groupby(['Intersection', 'Condition'])['rt'].mean()
#         sem_data = data.groupby(['Intersection', 'Condition'])['rt'].sem()

#         rt_data = pd.DataFrame()
#         rt_data['Intersection'] = grouped_data.index.get_level_values(0)
#         rt_data['Condition'] = grouped_data.index.get_level_values(1)
#         rt_data['rt'] = grouped_data.values

#         #save the average reaction time of each run to a new csv file
#         # output_file = os.path.join(aver_path, f'{os.path.splitext(csv_file)[0]}_aver_rt.csv')
#         # rt_data.to_csv(output_file, index=False)

#         if 'Repetition' in csv_file:
#             combined_repe_data = pd.concat([repe_data, rt_data], ignore_index=True)
#             repe_data = combined_repe_data
#         elif 'Retracing' in csv_file:
#             combined_retra_data = pd.concat([retra_data, rt_data], ignore_index=True)
#             retra_data = combined_retra_data

#     combined_repe_file = os.path.join(aver_path, f'{subject_dir}_repetition_combined_aver_rt.csv')
#     combined_retra_file = os.path.join(aver_path, f'{subject_dir}_retracing_combined_aver_rt.csv')
#     repe_data.to_csv(combined_repe_file, index=False)
#     retra_data.to_csv(combined_retra_file, index=False)

#     combined_repe = pd.read_csv(combined_repe_file)
#     grouped_data = combined_repe.groupby(['Intersection', 'Condition'])['rt'].mean()
#     sem_data = combined_repe.groupby(['Intersection', 'Condition'])['rt'].sem()
#     fig, ax2 = plt.subplots()
#     repe_Car_data = grouped_data.loc(axis=0)[:, 'Car']
#     repe_C2_data = grouped_data.loc(axis=0)[:, 'Intersection1']
#     repe_C3_data = grouped_data.loc(axis=0)[:, 'Intersection2']
#     plt.errorbar(repe_Car_data.index.get_level_values(0), repe_Car_data.values,
#                 yerr=sem_data.loc[('Intersection1', 'Car')], 
#                 marker='o', label='Start (car)', color='blue', linestyle='--')
#     plt.errorbar(repe_C2_data.index.get_level_values(0), repe_C2_data.values,
#                 yerr=sem_data.loc[('Intersection2', 'Intersection1')], 
#                 marker='s', label='Intersection1', color='red', linestyle='-')
#     plt.errorbar(repe_C3_data.index.get_level_values(0), repe_C3_data.values,
#                 yerr=sem_data.loc[('Intersection3', 'Intersection2')], 
#                 marker='v', label='Intersection2', color='green', linestyle='-')

#     plt.xlabel('Intersection', fontsize=16)
#     plt.ylabel('Reaction time (s)', fontsize=16)
#     box = ax2.get_position()
#     ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#     plt.ylim(0, 6)
#     plt.xticks(fontsize=14)
#     plt.yticks(fontsize=14)
#     plt.legend(loc='upper left', fontsize=12)  
#     figure_dir = os.path.join(figure_path, f'{subject_dir}_repetition_combined_aver_rt.png')
#     plt.savefig(figure_dir, transparent=True)
#     plt.show()

#     combined_retra = pd.read_csv(combined_retra_file)
#     grouped_data = combined_retra.groupby(['Intersection', 'Condition'])['rt'].mean()
#     sem_data = combined_retra.groupby(['Intersection', 'Condition'])['rt'].sem()
#     fig, ax2 = plt.subplots()
#     retra_Car_data = grouped_data.loc(axis=0)[:, 'PhoneBox']
#     retra_C2_data = grouped_data.loc(axis=0)[:, 'Intersection1']
#     retra_C3_data = grouped_data.loc(axis=0)[:, 'Intersection2']
#     plt.errorbar(retra_Car_data.index.get_level_values(0), retra_Car_data.values,
#                 yerr=sem_data.loc[('Intersection1', 'PhoneBox')], 
#                 marker='o', label='End (phone box)', color='blue', linestyle='--')
#     plt.errorbar(retra_C2_data.index.get_level_values(0), retra_C2_data.values,
#                 yerr=sem_data.loc[('Intersection2', 'Intersection1')], 
#                 marker='s', label='Intersection1', color='red', linestyle='-')
#     plt.errorbar(retra_C3_data.index.get_level_values(0), retra_C3_data.values,
#                 yerr=sem_data.loc[('Intersection3', 'Intersection2')], 
#                 marker='v', label='Intersection2', color='green', linestyle='-')
#     plt.xlabel('Intersection', fontsize=16)
#     plt.ylabel('Reaction time (s)', fontsize=16)
#     box = ax2.get_position()
#     ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#     plt.ylim(0, 6)
#     plt.xticks(fontsize=14)
#     plt.yticks(fontsize=14)
#     plt.legend(loc='upper left', fontsize=12)
#     figure_dir = os.path.join(figure_path, f'{subject_dir}_retracing_combined_aver_rt.png')
#     plt.savefig(figure_dir, transparent=True)
#     plt.show()

# Plot the average reaction time and accuracy for all subjects
import os
import matplotlib.pyplot as plt
import pandas as pd

base_dir = 'S:/GSani/JieSong/1.Data/raw_data'
figure_path = os.path.join(base_dir, 'figures')
aver_path = os.path.join(base_dir, 'figures', 'aver_rt_acc')
if not os.path.exists(figure_path):
    os.makedirs(figure_path)
# Iterate over each subject directory
for subject_dir in os.listdir(base_dir):
    if not subject_dir.startswith('sub'):
        continue
    input_dir = os.path.join(base_dir, subject_dir, 'condition_behavior')
    out_dir = os.path.join(base_dir, subject_dir, 'merged_behavior')
    
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
        
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
# Create a DataFrame to store the combined data for repetition and retracing
repe_data = pd.DataFrame()
retra_data = pd.DataFrame()
acc_repe_data = pd.DataFrame()
acc_retra_data = pd.DataFrame()
csv_files = [file for file in os.listdir(aver_path) if file.endswith('combined_aver_rt.csv')]
for csv_file in csv_files:
    csv_path = os.path.join(aver_path, csv_file)
    data = pd.read_csv(csv_path)
    grouped_data = data.groupby(['Intersection', 'Condition'])['rt'].mean()
    sem_data = data.groupby(['Intersection', 'Condition'])['rt'].sem()
    rt_data = pd.DataFrame()
    rt_data['Intersection'] = grouped_data.index.get_level_values(0)
    rt_data['Condition'] = grouped_data.index.get_level_values(1)
    rt_data['rt'] = grouped_data.values
    output_file = os.path.join(out_dir, f'{os.path.splitext(csv_file)[0]}_rt.csv')
    # Save the result to the output file
    rt_data.to_csv(output_file, index=False)
    if 'repetition' in csv_file:
        combined_repe_data = pd.concat([repe_data, rt_data], ignore_index=True)
        repe_data = combined_repe_data
    elif 'retracing' in csv_file:
        combined_retra_data = pd.concat([retra_data, rt_data], ignore_index=True)
        retra_data = combined_retra_data

combined_repe_file = os.path.join(aver_path, 'all_subjects_repetition_aver_rt.csv')
combined_retra_file = os.path.join(aver_path, 'all_subjects_retracing_aver_rt.csv')
repe_data.to_csv(combined_repe_file, index=False)
retra_data.to_csv(combined_retra_file, index=False)

combined_repe = pd.read_csv(combined_repe_file)
grouped_data = combined_repe.groupby(['Intersection', 'Condition'])['rt'].mean()
sem_data = combined_repe.groupby(['Intersection', 'Condition'])['rt'].sem()

fig, ax2 = plt.subplots()
repe_Car_data = grouped_data.loc(axis=0)[:, 'Car']
repe_C2_data = grouped_data.loc(axis=0)[:, 'Intersection1']
repe_C3_data = grouped_data.loc(axis=0)[:, 'Intersection2']
plt.errorbar(repe_Car_data.index.get_level_values(0), repe_Car_data.values,
            yerr=sem_data.loc[('Intersection1', 'Car')], 
            marker='o', label='Start (car)', color='blue', linestyle='--')
plt.errorbar(repe_C2_data.index.get_level_values(0), repe_C2_data.values,
            yerr=sem_data.loc[('Intersection2', 'Intersection1')], 
            marker='s', label='Intersection1', color='red', linestyle='-')
plt.errorbar(repe_C3_data.index.get_level_values(0), repe_C3_data.values,
            yerr=sem_data.loc[('Intersection3', 'Intersection2')], 
            marker='v', label='Intersection2', color='green', linestyle='-')

plt.xlabel('Intersection', fontsize=16)
plt.ylabel('Reaction time (s)', fontsize=16)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.ylim(0, 6)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc='upper left', fontsize=12)
figure_dir = os.path.join(figure_path, f'all_subjects_repetition_aver_rt.png')
plt.savefig(figure_dir, transparent=True)
plt.show()

combined_retra = pd.read_csv(combined_retra_file)
grouped_data = combined_retra.groupby(['Intersection', 'Condition'])['rt'].mean()
sem_data = combined_retra.groupby(['Intersection', 'Condition'])['rt'].sem()
fig, ax2 = plt.subplots()
retra_Car_data = grouped_data.loc(axis=0)[:, 'PhoneBox']
retra_C2_data = grouped_data.loc(axis=0)[:, 'Intersection1']
retra_C3_data = grouped_data.loc(axis=0)[:, 'Intersection2']
plt.errorbar(retra_Car_data.index.get_level_values(0), retra_Car_data.values,
            yerr=sem_data.loc[('Intersection1', 'PhoneBox')], 
            marker='o', label='End (phone box)', color='blue', linestyle='--')
plt.errorbar(retra_C2_data.index.get_level_values(0), retra_C2_data.values,
            yerr=sem_data.loc[('Intersection2', 'Intersection1')], 
            marker='s', label='Intersection1', color='red', linestyle='-')
plt.errorbar(retra_C3_data.index.get_level_values(0), retra_C3_data.values,
            yerr=sem_data.loc[('Intersection3', 'Intersection2')], 
            marker='v', label='Intersection2', color='green', linestyle='-')
plt.xlabel('Intersection', fontsize=16)
plt.ylabel('Reaction time (s)', fontsize=16)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.ylim(0, 6)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc='upper left', fontsize=12)
figure_dir = os.path.join(figure_path, f'all_subjects_retracing_aver_rt.png')
plt.savefig(figure_dir, transparent=True)
plt.show()



###### ACC
csv_files2 = [file for file in os.listdir(aver_path) if
                file.endswith('combined_aver_acc.csv')]

for csv_file in csv_files2:
    csv_path = os.path.join(aver_path, csv_file)
    data = pd.read_csv(csv_path)
    grouped_data = data.groupby(['Intersection', 'Condition'])['accuracy'].mean()
    sem_data = data.groupby(['Intersection', 'Condition'])['accuracy'].sem()
    acc_data = pd.DataFrame()
    acc_data['Intersection'] = grouped_data.index.get_level_values(0)
    acc_data['Condition'] = grouped_data.index.get_level_values(1)
    acc_data['accuracy'] = grouped_data.values
    if 'repetition' in csv_file:
        combined_repe_data = pd.concat([acc_repe_data, acc_data], ignore_index=True)
        acc_repe_data = combined_repe_data
    elif 'retracing' in csv_file:
        combined_retra_data = pd.concat([acc_retra_data, acc_data], ignore_index=True)
        acc_retra_data = combined_retra_data

combined_repe_file = os.path.join(aver_path, 'all_subjects_repetition_aver_acc.csv')
combined_retra_file = os.path.join(aver_path, 'all_subjects_retracing_aver_acc.csv')
acc_repe_data.to_csv(combined_repe_file, index=False)
acc_retra_data.to_csv(combined_retra_file, index=False)

combined_repe = pd.read_csv(combined_repe_file)
grouped_data = combined_repe.groupby(['Intersection', 'Condition'])['accuracy'].mean()
sem_data = combined_repe.groupby(['Intersection', 'Condition'])['accuracy'].sem()
fig, ax2 = plt.subplots()
repe_Car_data = grouped_data.loc(axis=0)[:, 'Car']
repe_C2_data = grouped_data.loc(axis=0)[:, 'Intersection1']
repe_C3_data = grouped_data.loc(axis=0)[:, 'Intersection2']
plt.errorbar(repe_Car_data.index.get_level_values(0), repe_Car_data.values,
            yerr=sem_data.loc[('Intersection1', 'Car')], 
            marker='o', label='Start (car)', color='blue', linestyle='--')
plt.errorbar(repe_C2_data.index.get_level_values(0), repe_C2_data.values,
            yerr=sem_data.loc[('Intersection2', 'Intersection1')], 
            marker='s', label='Intersection1', color='red', linestyle='-')
plt.errorbar(repe_C3_data.index.get_level_values(0), repe_C3_data.values,
            yerr=sem_data.loc[('Intersection3', 'Intersection2')], 
            marker='v', label='Intersection2', color='green', linestyle='-')

plt.xlabel('Intersection', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.ylim(0, 1.4)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc='upper left', fontsize=12)
figure_dir = os.path.join(figure_path, f'all_subjects_repetition_aver_acc.png')
plt.savefig(figure_dir, transparent=True)
plt.show()

combined_retra = pd.read_csv(combined_retra_file)
grouped_data = combined_retra.groupby(['Intersection', 'Condition'])['accuracy'].mean()
sem_data = combined_retra.groupby(['Intersection', 'Condition'])['accuracy'].sem()
fig, ax2 = plt.subplots()
retra_Car_data = grouped_data.loc(axis=0)[:, 'PhoneBox']
retra_C2_data = grouped_data.loc(axis=0)[:, 'Intersection1']
retra_C3_data = grouped_data.loc(axis=0)[:, 'Intersection2']
plt.errorbar(retra_Car_data.index.get_level_values(0), retra_Car_data.values,
            yerr=sem_data.loc[('Intersection1', 'PhoneBox')], 
            marker='o', label='End (phone box)', color='blue', linestyle='--')
plt.errorbar(retra_C2_data.index.get_level_values(0), retra_C2_data.values,
            yerr=sem_data.loc[('Intersection2', 'Intersection1')], 
            marker='s', label='Intersection1', color='red', linestyle='-')
plt.errorbar(retra_C3_data.index.get_level_values(0), retra_C3_data.values,
            yerr=sem_data.loc[('Intersection3', 'Intersection2')], 
            marker='v', label='Intersection2', color='green', linestyle='-')
plt.xlabel('Intersection', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.ylim(0, 1.4)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc='upper left', fontsize=12)
figure_dir = os.path.join(figure_path, f'all_subjects_retracing_aver_acc.png')
plt.savefig(figure_dir, transparent=True)
plt.show()