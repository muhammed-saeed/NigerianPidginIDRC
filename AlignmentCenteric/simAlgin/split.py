import os
def save_chunk(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for line in data:
            file.write(f"{line}\n")
def load_sentences(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]
def split_data_into_chunks(english_file, pcm_file, chunks_folder, num_chunks=20):
    if not os.path.exists(chunks_folder):
        os.makedirs(chunks_folder)
    else:
        print("you")
    english_sentences = load_sentences(english_file)
    pcm_sentences = load_sentences(pcm_file)
    chunk_size = len(english_sentences) // num_chunks
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < num_chunks - 1 else len(english_sentences)
        english_chunk = english_sentences[start_idx:end_idx]
        pcm_chunk = pcm_sentences[start_idx:end_idx]
        save_chunk(english_chunk, os.path.join(chunks_folder, f"english_chunk_{i+1}.txt"))
        save_chunk(pcm_chunk, os.path.join(chunks_folder, f"pcm_chunk_{i+1}.txt"))
english_file = "align/giza-py/extratedPCMAFterAlignments/english.txt"
pcm_file = "align/giza-py/extratedPCMAFterAlignments/pcm.txt"
chunks_folder = "/local/musaeed/NPIDRC/align/simAlgin/data/chunks20"
split_data_into_chunks(english_file, pcm_file, chunks_folder)
