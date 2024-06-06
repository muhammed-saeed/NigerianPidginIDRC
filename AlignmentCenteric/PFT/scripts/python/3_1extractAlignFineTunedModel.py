import os
import numpy as np
import pandas as pd
from datetime import datetime
from pdtb2 import CorpusReader
df = pd.read_csv('pdtb2_pcm.csv', low_memory=False)
with open('align/awesomealign/rawData/english.txt', 'r') as f:
    english_texts = f.readlines()
with open('align/awesomealign/rawData/pcm.txt', 'r') as f:
    pcm_texts = f.readlines()
with open("/local/musaeed/NPIDRC/align/awesomealign/rawData/english2pcmAlignmentFineTunedModelpostprocessedpidgin.txt", "r") as f:
    alignment_data = [line.strip().split() for line in f]
def get_word_indices_from_raw_text(raw_text, full_text):
    start_char_idx = full_text.find(raw_text)
    if start_char_idx == -1:
        return []
    end_char_idx = start_char_idx + len(raw_text)
    start_word_idx = full_text[:start_char_idx].count(' ')
    end_word_idx = full_text[:end_char_idx].count(' ')
    return list(range(start_word_idx, end_word_idx + 1))
def get_aligned_indices(start_idx, end_idx, alignment):
    pcm_indices = []
    for i in range(start_idx, end_idx + 1):
        aligned_pairs = [pair for pair in alignment if int(pair.split('-')[0]) == i]
        for pair in aligned_pairs:
            _, pcm_idx = pair.split('-')
            pcm_indices.append(int(pcm_idx))
    return pcm_indices
def extract_words_from_indices(word_indices, text):
    words = text.split()
    return ' '.join(words[idx] for idx in word_indices)
corpus_reader = CorpusReader('/local/musaeed/pdtb2.csv')
arg1_rawtexts = []
arg2_rawtexts = []
connective_rawtexts = []
FullRawText = []
Relation = []
section = []
file_number = []
conn_head_sem_class1 = []
conn_head_sem_class2 = []
conn2_sem_class1 = []
conn2_sem_class2 = []
SentenceNumber = []
Conn1 = []
Conn2 = []
for datum in corpus_reader.iter_data(display_progress=False):
    arg1_rawtexts.append(datum.Arg1_RawText)
    arg2_rawtexts.append(datum.Arg2_RawText)
    connective_rawtexts.append(datum.Connective_RawText)
    FullRawText.append(datum.FullRawText)
    Relation.append(datum.Relation)
    section.append(datum.Section)
    file_number.append(datum.FileNumber)
    conn_head_sem_class1.append(datum.ConnHeadSemClass1)
    conn_head_sem_class2.append(datum.ConnHeadSemClass2)
    conn2_sem_class1.append(datum.Conn2SemClass1)
    conn2_sem_class2.append(datum.Conn2SemClass2)
    SentenceNumber.append(datum.SentenceNumber)
    Conn1.append(datum.Conn1)
    Conn2.append(datum.Conn2)
column_names = ['FullRawText','Arg1_RawText','Arg2_RawText','Connective_RawText','arg1_rawTextPCM_alignment', 'arg2_raw_textPCM_alignment', 'connective_rawTextPCM_alignment', 'Relation']
df['Arg1_RawText'] = arg1_rawtexts
df['Arg2_RawText'] = arg2_rawtexts
df['Connective_RawText'] = connective_rawtexts
df['FullRawText'] = FullRawText
df['Relation'] = Relation
df['Section'] = section
df['FileNumber'] = file_number
df['ConnHeadSemClass1'] = conn_head_sem_class1
df['ConnHeadSemClass2'] = conn_head_sem_class2
df['Conn2SemClass1'] = conn2_sem_class1
df['Conn2SemClass2'] = conn2_sem_class2
df['SentenceNumber'] = SentenceNumber
df['FullRawTextPCM'] = pcm_texts
df['Conn1'] = Conn1
df['Conn2'] =  Conn2
df['arg1_rawTextPCM_alignment'] = [None] * len(df)
df['arg2_raw_textPCM_alignment'] = [None] * len(df)
df['connective_rawTextPCM_alignment'] = [None] * len(df)
print(df.head())
desired_column_order = ["Relation", "Section", "FileNumber", "SentenceNumber", 
            "ConnHeadSemClass1", "ConnHeadSemClass2", 
            "Conn2SemClass1", "Conn2SemClass2", "Conn1", "Conn2"
            "Arg1_RawText", "Arg2_RawText", "FullRawText", "Connective_RawText", "FullRawTextPCM"]
for idx, row in df.iterrows():
    english_text = english_texts[idx]
    arg1_word_indices = get_word_indices_from_raw_text(row['Arg1_RawText'], english_text)
    arg2_word_indices = get_word_indices_from_raw_text(row['Arg2_RawText'], english_text)
    if not arg1_word_indices:
        df.at[idx, 'arg1_rawTextPCM_alignment'] = "Text Not Found"
    else:
        arg1_start, arg1_end = arg1_word_indices[0], arg1_word_indices[-1]
        pcm_indices_arg1 = get_aligned_indices(arg1_start, arg1_end, alignment_data[idx])
        if not pcm_indices_arg1:
            df.at[idx, 'arg1_rawTextPCM_alignment'] = "ALIGNMENT Error"
        else:
            df.at[idx, 'arg1_rawTextPCM_alignment'] = extract_words_from_indices(pcm_indices_arg1, pcm_texts[idx])
    if not arg2_word_indices:
        df.at[idx, 'arg2_raw_textPCM_alignment'] = "Text Not Found"
    else:
        arg2_start, arg2_end = arg2_word_indices[0], arg2_word_indices[-1]
        pcm_indices_arg2 = get_aligned_indices(arg2_start, arg2_end, alignment_data[idx])
        if not pcm_indices_arg2:
            df.at[idx, 'arg2_raw_textPCM_alignment'] = "ALIGNMENT Error"
        else:
            df.at[idx, 'arg2_raw_textPCM_alignment'] = extract_words_from_indices(pcm_indices_arg2, pcm_texts[idx])
    connective = row['Connective_RawText']
    relation = row['Relation']
    if pd.isna(connective) or relation == "Implicit":  
        df.at[idx, 'connective_rawTextPCM_alignment'] = np.nan  
    else:
        connective_word_indices = get_word_indices_from_raw_text(connective, english_text)
        if not connective_word_indices:
            df.at[idx, 'connective_rawTextPCM_alignment'] = "Text Not Found"
        else:
            connective_start, connective_end = connective_word_indices[0], connective_word_indices[-1]
            pcm_indices_connective = get_aligned_indices(connective_start, connective_end, alignment_data[idx])
            if not pcm_indices_connective:
                df.at[idx, 'connective_rawTextPCM_alignment'] = "ALIGNMENT Error"
            else:
                df.at[idx, 'connective_rawTextPCM_alignment'] = extract_words_from_indices(pcm_indices_connective, pcm_texts[idx])
variants_df = pd.read_csv("align/simAlgin/data/variants.csv")
def find_variant1(connective_rawtext):
    for i in range(1, 8):
        et_column = f"ET{i}" 
        variant_column = f"variant1"  
        et_value = connective_rawtext  
        if et_value in variants_df[et_column].values:
            variant1_value = variants_df.loc[variants_df[et_column] == et_value, variant_column].values[0]
            return variant1_value
    return None  
for idx, row in df.iterrows():
    english_text = english_texts[idx]
    if row['connective_rawTextPCM_alignment'] == "ALIGNMENT Error":
        connective_rawtext = row['Connective_RawText']
        variant1 = find_variant1(connective_rawtext)
        if variant1 is not None:
            df.at[idx, 'connective_rawTextPCM_alignment'] = variant1
current_date = datetime.now().strftime("%Y%m%d")
folder_path = f'align/awesomealign/data/TextError/FineTunedModel/{current_date}'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
print(f"Folder '{folder_path}' has been created.")
arg1_raw_textPCM_alignment = df['arg1_rawTextPCM_alignment']
arg2_raw_textPCM_alignment = df['arg2_raw_textPCM_alignment']
connective_raw_textPCM_alignment = df['connective_rawTextPCM_alignment']  
ARG1_RawText = df['Arg1_RawText']
ARG2_RawText = df['Arg2_RawText']
English_Fulltext = df['FullRawText']
Relation = df['Relation']
PidginFullText = df['FullRawTextPCM']
combined_path = f'align/awesomealign/data/TextError/FineTunedModel/{current_date}/combined'
value_counts = df['connective_rawTextPCM_alignment'].value_counts()
df.to_csv(f'{folder_path}/pdtb2_pcm_alignment_naijaLex_soft.csv', index=False)
combined_df = pd.DataFrame({
    'arg1_rawTextPCM_alignment': arg1_raw_textPCM_alignment,
    'arg2_raw_textPCM_alignment': arg2_raw_textPCM_alignment,
    'connective_rawTextPCM_alignment': connective_raw_textPCM_alignment,  
    'FullRawText': English_Fulltext,
    'Relation':Relation,
    'PidginFullRawText': PidginFullText
})
if not os.path.exists(combined_path):
    os.makedirs(combined_path)
combined_df.to_csv(f'{combined_path}/combined_columns_alignments_soft.csv', index=False)
with open(f'{combined_path}/connective_alignment_afterNaijaLexProcessing_unique_values.txt', 'w') as file:
    for value, count in value_counts.items():
        file.write(f"{value}: {count}\n")
print("Unique values and counts saved to ' naija lex processing connective_alignment_unique_values.txt'")
value_counts = df['Connective_RawText'].value_counts()
with open(f'{combined_path}/connective_englishRawtext_afterNaijaLexProcessing_unique_values.txt', 'w') as file:
    for value, count in value_counts.items():
        file.write(f"{value}: {count}\n")
print("Unique values and counts saved to ' naija lex processing connective_alignment_unique_values.txt'")
