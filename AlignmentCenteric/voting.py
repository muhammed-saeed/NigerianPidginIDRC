alignment_files = [
    "/local/musaeed/NPIDRC/align/fastAlign/data/translatedData/alignments.txt",
    "/local/musaeed/NPIDRC/align/eflomal/data/translatedData/alignments.txt",
    "/local/musaeed/NPIDRC/align/giza-py/extratedPCMAFterAlignments/English2PCMalignments.txt",
    "/local/musaeed/NPIDRC/align/simAlgin/data/alignments_output.txt"
]


alignment_lines_lists = []
for file_path in alignment_files:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        alignment_lines_lists.append(lines)


alignment_counts = {}


for alignment_lines in alignment_lines_lists:
    for line in alignment_lines:
        if line in alignment_counts:
            alignment_counts[line] += 1
        else:
            alignment_counts[line] = 1


most_common_alignment = None
for line, count in alignment_counts.items():
    if count >= 3:
        most_common_alignment = line
        break


if most_common_alignment:
    output_alignment = most_common_alignment
else:
    
    output_alignment = alignment_lines_lists[-1][-1]


output_file_path = "/local/musaeed/NPIDRC/align/alignments_voting.txt"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(output_alignment + "\n")

print(f"Generated 'alignments_voting.txt' with the selected alignment: {output_alignment}")
