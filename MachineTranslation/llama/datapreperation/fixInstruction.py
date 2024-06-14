import argparse
import json
import os

def replace_instructions(json_file, output_directory):
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Iterate over each object in the JSON array
    for obj in data:
        instruction = obj.get('instruction', '')

        # Replace specific values
        if instruction == 'translate english to pcm':
            obj['instruction'] = 'translate English to Nigerian Pidgin'
        elif instruction == 'translate pcm to english':
            obj['instruction'] = 'translate Nigerian Pidgin to English'
       
    # Convert the modified data back to JSON string
    updated_json_data = json.dumps(data)

    # Specify the file path for the output file
    
    output_file = output_directory

    # Save the updated JSON data to the output file
    with open(output_file, 'w') as file:
        file.write(updated_json_data)

    print(f"The file has been saved to: {output_file}")


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Replace instructions in a JSON file.')

    # Add the command-line arguments
    parser.add_argument('--json_file', default="llama/data/bidirectional_translation.json", help='Path to the JSON file')
    parser.add_argument('--output_directory', default="llama/data/bidirectional_translation_fixed_instruction.json", help='Path to the output directory')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to replace instructions
    replace_instructions(args.json_file, args.output_directory)
