import json
import random
import argparse

def sample_json_file(json_file, sample_size, output_file):
    # Open the JSON file and load the data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Randomly sample a few entries
    sampled_entries = random.sample(data, sample_size)

    # Save the sampled entries to a new file
    with open(output_file, 'w') as f:
        json.dump(sampled_entries, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample a few entries from a JSON file and save them to a new file.")
    parser.add_argument("-j", "--json", help="JSON file to sample from", default="/PATH_TO/general-pidgin-modeling/llamma/data/bidirectional_translation.json")
    parser.add_argument("-s", "--size", help="Number of entries to sample", type=int, default=5)
    parser.add_argument("-o", "--output", help="Output file to save the sampled entries", default="/PATH_TO/general-pidgin-modeling/llamma/data/sample_bidirectional_translation.json")

    args = parser.parse_args()

    sample_json_file(args.json, args.size, args.output)
