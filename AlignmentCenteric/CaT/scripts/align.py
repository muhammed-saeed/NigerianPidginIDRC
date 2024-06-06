import torch
from transformers import RobertaTokenizer, RobertaModel
from sklearn.metrics.pairwise import cosine_similarity


tokenizer_en = RobertaTokenizer.from_pretrained('roberta-base')
model_en = RobertaModel.from_pretrained('roberta-base')

tokenizer_pidgin = RobertaTokenizer.from_pretrained('roberta-base')
model_pidgin = RobertaModel.from_pretrained('/local/musaeed/checkpoint-53500')


english_sentence = "Hello, how are you?"
pidgin_sentence = "How you dey?"


encoded_en = tokenizer_en(english_sentence, return_tensors='pt', padding=True, truncation=True)
encoded_pidgin = tokenizer_pidgin(pidgin_sentence, return_tensors='pt', padding=True, truncation=True)


with torch.no_grad():
    embeddings_en = model_en(**encoded_en).last_hidden_state.mean(dim=1).tolist()
    embeddings_pidgin = model_pidgin(**encoded_pidgin).last_hidden_state.mean(dim=1).tolist()


similarity_matrix = cosine_similarity(embeddings_en, embeddings_pidgin)


similarity_threshold = 0.8


aligned_word_pairs = []
for en_idx, en_emb in enumerate(embeddings_en):
    for pidgin_idx, pidgin_emb in enumerate(embeddings_pidgin):
        similarity_score = cosine_similarity([en_emb], [pidgin_emb])[0][0]
        if similarity_score >= similarity_threshold:
            aligned_word_pairs.append((en_idx, pidgin_idx))


en_words = tokenizer_en.convert_ids_to_tokens(encoded_en.input_ids[0])
pidgin_words = tokenizer_pidgin.convert_ids_to_tokens(encoded_pidgin.input_ids[0])

for en_idx, pidgin_idx in aligned_word_pairs:
    if en_words[en_idx] != "<s>" and pidgin_words[pidgin_idx] != "<s>":
        print(f"{en_words[en_idx]}-{pidgin_words[pidgin_idx]}")
