import glob
import os
import pandas as pd

# Step 1: Find and filter the CSV files
base_dir = 'S:/GSani/JieSong/1.Data/raw_data'
input_dir = f'{base_dir}/*/unity_behavior'
# input_files = glob.glob(f"{input_dir}/PILOT12_RepRet_Run*_*_*_Timeline.csv")
input_files = glob.glob(f"{input_dir}/sub04_RepRet_Run*_*_*.csv")
out_dir = f'{base_dir}/sub04/merged_behavior'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
# Step 2: Define a function to merge and save files for each run
def merge_and_save(files, run_number):
    run_files_01 = [file for file in files if f"Run{run_number:02}_01_" in file]
    run_files_02 = [file for file in files if f"Run{run_number:02}_02_" in file]
    
    # Read the first file
    df1 = pd.read_csv(run_files_01[0], header=None, sep='\t')
    
    # Read the second file
    df2 = pd.read_csv(run_files_02[0], header=None, sep='\t')
    
    # # Add title row to df1
    # title_row = pd.Series(["Timestamp", "Events_ID", "Events", "Response"])
    # df1 = pd.concat([title_row.to_frame().T, df1], ignore_index=True)
    
    # Concatenate df1 above df2
    merged_df = pd.concat([df1, df2], ignore_index=True)
    
    merged_file_path = os.path.join(out_dir, f"sub04_RepRet_Run{run_number:02}.csv")
    merged_df.to_csv(merged_file_path, index=False, header=False, sep='\t')
    print(f"Merged dataframe saved to: {merged_file_path}")

# Step 3: Iterate over the runs (assuming 6 runs)
for run_number in range(1, 7):
    merge_and_save(input_files, run_number)

