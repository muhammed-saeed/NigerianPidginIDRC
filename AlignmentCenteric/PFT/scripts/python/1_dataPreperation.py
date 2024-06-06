import argparse
def combine_files(source_file, target_file, output_file):
    with open(source_file, 'r', encoding='utf-8') as src_file, \
         open(target_file, 'r', encoding='utf-8') as tgt_file, \
         open(output_file, 'w', encoding='utf-8') as out_file:
        for src_line, tgt_line in zip(src_file, tgt_file):
            combined_line = f'{src_line.strip()} ||| {tgt_line.strip()}\n'
            out_file.write(combined_line)
def main():
    parser = argparse.ArgumentParser(description='Combine source and target text files.')
    parser.add_argument('--source', '-s', type=str, help='Path to the source text file', required=True)
    parser.add_argument('--target', '-t', type=str, help='Path to the target text file', required=True)
    parser.add_argument('--output', '-o', type=str, help='Path to the output file', required=True)
    args = parser.parse_args()
    combine_files(args.source, args.target, args.output)
    print(f"Combined lines written to {args.output}")
if __name__ == "__main__":
    main()
