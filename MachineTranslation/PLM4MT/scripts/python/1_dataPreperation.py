import argparse

def create_translation_files(en_file_path, pcm_file_path, output_en_pcm_path, output_pcm_en_path, output_bidirectional_path):
    with open(en_file_path, 'r') as en_file, \
         open(pcm_file_path, 'r') as pcm_file, \
         open(output_en_pcm_path, 'w') as output_en_pcm_file, \
         open(output_pcm_en_path, 'w') as output_pcm_en_file, \
         open(output_bidirectional_path, 'w') as output_bidirectional_file:

        # Read lines from English and Pidgin files
        en_lines = en_file.readlines()
        pcm_lines = pcm_file.readlines()

        # Ensure both files have the same number of lines
        if len(en_lines) != len(pcm_lines):
            raise ValueError("Number of lines in English and Pidgin files must be the same.")

        # Write translations into separate files
        for en_line, pcm_line in zip(en_lines, pcm_lines):
            en_sentence = en_line.strip()
            pcm_sentence = pcm_line.strip()

            # Write English to Pidgin translation
            output_en_pcm_file.write(f"<extra_id_5> {en_sentence} <extra_id_0> {pcm_sentence}\n")

            # Write Pidgin to English translation
            output_pcm_en_file.write(f"<extra_id_5> {pcm_sentence} <extra_id_0> {en_sentence}\n")

            # Write bidirectional translation
            output_bidirectional_file.write(f"<extra_id_5> {en_sentence} <extra_id_0> {pcm_sentence}\n")
            output_bidirectional_file.write(f"<extra_id_5> {pcm_sentence} <extra_id_0> {en_sentence}\n")

def main():
    parser = argparse.ArgumentParser(description="Create translation files for English to Pidgin, Pidgin to English, and bidirectional translations.")
    parser.add_argument("--en_file", default="/PATH_TO/PLM4MT/data/textFiles/BibleJw300TreeBankShuffled.en", help="Path to the English file")
    parser.add_argument("--pcm_file", default="/PATH_TO/PLM4MT/data/textFiles/BibleJw300TreeBankShuffled.pcm", help="Path to the Pidgin file")
    parser.add_argument("--output_en_pcm", default="/PATH_TO/PLM4MT/data/textFiles/BibleJw300TreeBankShuffled.en2pcm", help="Path to the output English to Pidgin file")
    parser.add_argument("--output_pcm_en", default="/PATH_TO/PLM4MT/data/textFiles/BibleJw300TreeBankShuffled.pcm2en", help="Path to the output Pidgin to English file")
    parser.add_argument("--output_bidirectional", default="/PATH_TO/PLM4MT/data/textFiles/BibleJw300TreeBankShuffled.enpcmbidirectional", help="Path to the output bidirectional file")

    args = parser.parse_args()

    create_translation_files(args.en_file, args.pcm_file, args.output_en_pcm, args.output_pcm_en, args.output_bidirectional)

if __name__ == "__main__":
    main()
