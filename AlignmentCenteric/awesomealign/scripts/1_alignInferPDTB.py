from tqdm import tqdm
from simalign import SentenceAligner



myaligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")


with open("align/giza-py/extratedPCMAFterAlignments/english.txt", "r", encoding="utf-8") as f:
    english_sentences = [line.strip() for line in f.readlines()]


with open("align/giza-py/extratedPCMAFterAlignments/pcm.txt", "r", encoding="utf-8") as f:
    pcm_sentences = [line.strip() for line in f.readlines()]


alignments_list = []


total_sentences = len(english_sentences)
with tqdm(total=total_sentences, desc="Aligning sentences") as pbar:
    
    for english_sent, pcm_sent in zip(english_sentences, pcm_sentences):
        
        alignments = myaligner.get_word_aligns(english_sent.split(), pcm_sent.split())

        
        alignment_pairs = alignments["mwmf"]
        formatted_alignments = [f"{src_idx}-{trg_idx}" for src_idx, trg_idx in alignment_pairs]
        formatted_output = " ".join(formatted_alignments)

        
        alignments_list.append(formatted_output)

        pbar.update(1)  


with open("align/simAlgin/data/simAlign_alignments_output.txt", "w", encoding="utf-8") as f:
    for alignment in alignments_list:
        f.write(f"{alignment}\n")
