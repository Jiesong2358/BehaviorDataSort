import csv
import os
import re

# Folder containing the source files
processed_files_directory = "/Users/marie-eliselatorre/Downloads/LabNIC/ProcessedFiles"
out_dir = os.path.join(processed_files_directory, 'Group_analysis')
# Folders for saving the processed event files
encoding_directory = "encoding"
retrieval_directory = "retrieval"

# Create the folders if they do not exist
os.makedirs(encoding_directory, exist_ok=True)
os.makedirs(retrieval_directory, exist_ok=True)

def extract_run_number(filename):
    match = re.search(r"Run(\d+)", filename)
    if match:
        return match.group(1)
    return None

def process_encoding_events(events, mri_sync_time):
    results = []
    for event in events:
        if "Dir_Encoding_Start" in event[2] or "Rep1_Encoding_Start" in event[2]:
            onset = (event[0] - mri_sync_time) / 1000  # Convert to seconds
            duration = 4  # Duration is always 4 seconds for encoding
            trial_type = "allo_encoding" if "Dir_Encoding_Start" in event[2] else "ego_encoding"
            results.append([onset, duration, trial_type])
    return results

def process_retrieval_events(events, mri_sync_time):
    results = []
    response_times = {}
    for event in events:
        if "Rep1_IntersectionStop" in event[2] or "Dir_Intersection_Stop" in event[2]:
            intersection_stop_time = event[0]
            for response_event in events:
                if "Rep1_Response" in response_event[2] or "Dir_Response" in response_event[2]:
                    if response_event[0] > intersection_stop_time:
                        response_time = (response_event[0] - intersection_stop_time) / 1000
                        response_times[intersection_stop_time] = response_time
                        break

    for event in events:
        if "Rep1_IntersectionStop" in event[2] or "Dir_Intersection_Stop" in event[2]:
            onset = (event[0] - mri_sync_time) / 1000  # Convert to seconds
            duration = 4 if "Dir" in event[2] else 2  # 4 seconds for directional, 2 for repetition
            trial_type = "allo_encoding" if "Dir" in event[2] else "ego_encoding"
            response_time = response_times.get(event[0], None)
            results.append([onset, duration, trial_type, response_time])
    return results

run_data_dict = {"encoding": {}, "retrieval": {}}  # Dictionary to store data for each run

for filename in os.listdir(processed_files_directory):
    if filename.endswith(".csv"):
        run_number = extract_run_number(filename)
        file_path = os.path.join(processed_files_directory, filename)

        mri_sync_time = None
        events = []

        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    timestamp = float(row[0])
                    event_type = row[2] if len(row) > 2 else ""
                    if '[MRI_Sync]' in event_type:
                        mri_sync_time = timestamp
                    elif 'Dir_Encoding_Start' in event_type or 'Rep1_Encoding_Start' in event_type or \
                         'Rep1_IntersectionStop' in event_type or 'Dir_Intersection_Stop' in event_type or \
                         'Rep1_Response' in event_type or 'Dir_Response' in event_type:
                        events.append((timestamp, float(row[1]) if len(row) > 1 else None, event_type))
                except ValueError:
                    continue

        if mri_sync_time is not None:
            encoding_events = [event for event in events if 'Dir_Encoding_Start' in event[2] or 'Rep1_Encoding_Start' in event[2]]
            retrieval_events = [event for event in events if 'Rep1_IntersectionStop' in event[2] or 'Dir_Intersection_Stop' in event[2] or 'Rep1_Response' in event[2] or 'Dir_Response' in event[2]]

            if run_number not in run_data_dict["encoding"]:
                run_data_dict["encoding"][run_number] = []
            run_data_dict["encoding"][run_number].extend(process_encoding_events(encoding_events, mri_sync_time))

            if run_number not in run_data_dict["retrieval"]:
                run_data_dict["retrieval"][run_number] = []
            run_data_dict["retrieval"][run_number].extend(process_retrieval_events(retrieval_events, mri_sync_time))

# Write each run's data to a separate CSV file in the appropriate folder
for phase in run_data_dict:
    for run_number, data in run_data_dict[phase].items():
        if phase == "encoding":
            results_csv_file = os.path.join(encoding_directory, f"consolidated_results_run_{run_number}.csv")
            with open(results_csv_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['onset', 'duration', 'trial_type'])
                for row in data:
                    writer.writerow([run_number] + row)  # Include run number in output

            print(f"Consolidated encoding results for Run {run_number} saved in {results_csv_file}.")
        
        elif phase == "retrieval":
            results_csv_file = os.path.join(retrieval_directory, f"consolidated_results_run_{run_number}.csv")
            with open(results_csv_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['onset', 'duration', 'trial_type', 'response_time'])
                for row in data:
                    writer.writerow([run_number] + row)  # Include run number in output

            print(f"Consolidated retrieval results for Run {run_number} saved in {results_csv_file}.")
