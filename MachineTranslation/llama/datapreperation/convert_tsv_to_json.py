import argparse
import pandas as pd

def convert_tsv_to_json(input_file, output_file):
    # load the tsv file
    df = pd.read_csv(input_file, sep='\t')

    # rename the columns as necessary
    df = df.rename(columns={'prefix': 'instruction', 'input_text': 'input', 'target_text': 'output'})

    # convert the DataFrame to a JSON file
    df.to_json(output_file, orient='records')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a TSV file to a JSON file and rename columns.")
    parser.add_argument("-i", "--input", help="Input TSV file", default="/PATH_TO/train.tsv")
    parser.add_argument("-o", "--output", help="Output JSON file", default="/PATH_TO/general-pidgin-modeling/llamma/data/bidirectional_translation.json")

    args = parser.parse_args()

  

    convert_tsv_to_json(args.input, args.output)

