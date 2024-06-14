import argparse
import pandas as pd

def sample_tsv_file(file_name, num_samples, output_file):
    # Load the tsv file
    df = pd.read_csv(file_name, sep='\t')

    # Sample a few rows from the DataFrame
    sampled_df = df.sample(n=num_samples)

    sampled_df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample a few lines from a TSV file.")
    parser.add_argument("-f", "--file", help="TSV file to sample from", default="/PATH_TO/train.tsv")
    parser.add_argument("-n", "--num", help="Number of lines to sample", type=int, default=5)
    parser.add_argument("--output_file", default="/PATH_TO/sample.tsv")

    args = parser.parse_args()

    sampled_df = sample_tsv_file(args.file, args.num, args.output_file)

    # Print the sampled lines
    
