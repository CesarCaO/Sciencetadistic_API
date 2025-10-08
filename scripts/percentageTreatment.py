import json
import os

json_path= "./Deprecated/"
langFile = os.listdir(json_path) 
save_path="./JSON_Metrics/"

for file in langFile:
    print(file)
    file_path = os.path.join(json_path,file)
    with open(file_path, "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)

        if 'Accepted' not in data or 'Rejected' not in data:
            print(f"Warning: Missing required keys in {file}")
            continue

        accepted = [x/100 for x in data['Accepted']]
        rejected = [x/100 for x in data['Rejected']]

        newJson = {
            'Accepted': accepted,
            'Rejected': rejected
        }

        output_path = os.path.join(save_path, file)
        with open(output_path, "w", encoding="utf-8") as outFile:
            json.dump(newJson, outFile, indent=4)
