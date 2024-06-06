from tqdm import tqdm
from simalign import SentenceAligner
from transformers import RobertaTokenizerFast
import concurrent.futures


model_checkpoint = "/local/musaeed/checkpoint-53500"
tokenizer = RobertaTokenizerFast.from_pretrained(model_checkpoint, add_prefix_space=True)
tokenizer.save_pretrained(model_checkpoint)
k = 100

myaligner = SentenceAligner(model=model_checkpoint, token_type="bpe", matching_methods="mai")


def preprocess_sentences(english_sentences, pcm_sentences):
    tokenized_sentences = []
    for english_sent, pcm_sent in zip(english_sentences, pcm_sentences):
        eng_tokens = tokenizer.tokenize(english_sent)
        pcm_tokens = tokenizer.tokenize(pcm_sent)
        tokenized_sentences.append((eng_tokens, pcm_tokens))
    return tokenized_sentences


def process_tokenized_sentences_chunk(tokenized_sentences_chunk, chunk_index):
    alignments_list = []
    for eng_tokens, pcm_tokens in tokenized_sentences_chunk:
        alignments = myaligner.get_word_aligns(eng_tokens, pcm_tokens)
        alignment_pairs = alignments["mwmf"]
        formatted_alignments = [f"{src_idx}-{trg_idx}" for src_idx, trg_idx in alignment_pairs]
        alignments_list.append(" ".join(formatted_alignments))

    
    with open(f"align/simAlgin/data/chunks/part_{chunk_index}.txt", "w", encoding="utf-8") as f:
        for alignment in alignments_list:
            f.write(f"{alignment}\n")


with open("align/giza-py/extratedPCMAFterAlignments/english.txt", "r", encoding="utf-8") as f:
    english_sentences = [line.strip() for line in f.readlines()][:k]

with open("align/giza-py/extratedPCMAFterAlignments/pcm.txt", "r", encoding="utf-8") as f:
    pcm_sentences = [line.strip() for line in f.readlines()][:k]


tokenized_sentences = preprocess_sentences(english_sentences, pcm_sentences)


chunk_size = 10  


tokenized_chunks = [tokenized_sentences[i:i + chunk_size] for i in range(0, len(tokenized_sentences), chunk_size)]


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_tokenized_sentences_chunk, chunk, idx) for idx, chunk in enumerate(tokenized_chunks)]
    for future in concurrent.futures.as_completed(futures):
        future.result()


with open("align/simAlgin/data/simAlign_alignments_outputRobertaPCM_combined.txt", "w", encoding="utf-8") as outfile:
    for i in range(len(tokenized_chunks)):
        with open(f"align/simAlgin/data/chunks/part_{i}.txt", "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
