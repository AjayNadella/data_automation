import csv
import os

def write_to_csv(data: dict, output_path: str):
    
    file_exists = os.path.isfile(output_path)

    with open(output_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)
