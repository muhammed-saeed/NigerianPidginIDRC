import os
import numpy as np
import pandas as pd
from datetime import datetime
from pdtb2 import CorpusReader
df = pd.read_csv('/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/DisContinousImplicitpdtb2ExtractedWithPostProecessingTranslation.csv', low_memory=False)
with open('/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/awesome/englishBERTAlignment/EnglishBERTDiscontinousImpEntrelenglish.txt', 'r') as f:
    english_texts = f.readlines()
with open("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/awesome/englishBERTAlignment/EnglishBERTDiscontinousImpEntrelpidgin.txt", "r") as f:
    pcm_texts = f.readlines()
with open("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/awesome/englishBERTAlignment/EnglishBERTfiltered_alignmentsPCM2EN.txt", "r") as f:
    alignment_data = [line.strip().split() for line in f]
def get_word_indices_from_raw_text(ArgConnRaw_text, full_text):
    start_char_idx = full_text.find(ArgConnRaw_text)
    if start_char_idx == -1:
        return []
    end_char_idx = start_char_idx + len(ArgConnRaw_text)
    start_word_idx = full_text[:start_char_idx].count(' ')
    end_word_idx = full_text[:end_char_idx].count(' ')
    return list(range(start_word_idx, end_word_idx + 1))
def get_aligned_indices(eng_start_idx, eng_end_idx, alignment):
    """
    Given a range of English word indices (from eng_start_idx to eng_end_idx),
    find the corresponding Pidgin indices based on alignment data structured as 'pidgin_idx-english_idx'.
    :param eng_start_idx: int, start index in English text
    :param eng_end_idx: int, end index in English text
    :param alignment: list of strings, where each string is "pidgin_idx-english_idx"
    :return: list of ints, corresponding indices in the Pidgin text
    """
    pcm_indices = []
    for i in range(eng_start_idx, eng_end_idx + 1):
        aligned_pairs = [pair for pair in alignment if int(pair.split('-')[1]) == i]
        for pair in aligned_pairs:
            pcm_idx, _ = pair.split('-')
            pcm_indices.append(int(pcm_idx))
    return pcm_indices
def get_aligned_indicesEn2PCM(start_idx, end_idx, alignment):
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
dfprocess = pd.read_csv('/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/DisContinousImplicitpdtb2ExtractedWithPostProecessingTranslation.csv', low_memory=False)
dfprocess['Arg1_RawText'] = dfprocess['Arg1_RawTextExtracted']
dfprocess['Arg2_RawText'] = dfprocess['Arg2_RawTextExtracted']
dfprocess['FullRawText'] = dfprocess['FullRawTextExtracted']
dfprocess.to_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/DisContinousImplicitpdtb2ExtractedWithPostProecessingTranslationForCode.csv", index=False)
df = pd.read_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/DisContinousImplicitpdtb2ExtractedWithPostProecessingTranslationForCode.csv", low_memory=False)
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
column_names = ['FullRawText','Arg1_RawText','Arg2_RawText','Connective_RawText','Arg1_RawTextPCM_Alignment', 'Arg2_RawTextPCM_Alignment', 'Connective_RawTextPCM_Alignment', 'Relation']
df['Connective_RawText'] = [connective_rawtexts[i] for i in df['original_index']]
df['Relation'] = [Relation[i] for i in df['original_index']]
df['Section'] = [section[i] for i in df['original_index']]
df['FileNumber'] = [file_number[i] for i in df['original_index']]
df['ConnHeadSemClass1'] = [conn_head_sem_class1[i] for i in df['original_index']]
df['ConnHeadSemClass2'] = [conn_head_sem_class2[i] for i in df['original_index']]
df['Conn2SemClass1'] = [conn2_sem_class1[i] for i in df['original_index']]
df['Conn2SemClass2'] = [conn2_sem_class2[i] for i in df['original_index']]
df['SentenceNumber'] = [SentenceNumber[i] for i in df['original_index']]
df['FullRawTextPCM'] = pcm_texts
df['Conn1'] = [Conn1[i] for i in df['original_index']]
df['Conn2'] = [Conn2[i] for i in df['original_index']]
df['Arg1_RawTextPCM_Alignment'] = [None] * len(df)
df['Arg2_RawTextPCM_Alignment'] = [None] * len(df)
df['Connective_RawTextPCM_Alignment'] = [None] * len(df)
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
        df.at[idx, 'Arg1_RawTextPCM_Alignment'] = "Text Not Found"
    else:
        arg1_start, arg1_end = arg1_word_indices[0], arg1_word_indices[-1]
        pcm_indices_arg1 = get_aligned_indices(arg1_start, arg1_end, alignment_data[idx])
        if not pcm_indices_arg1:
            df.at[idx, 'Arg1_RawTextPCM_Alignment'] = "ALIGNMENT Error"
        else:
            df.at[idx, 'Arg1_RawTextPCM_Alignment'] = extract_words_from_indices(pcm_indices_arg1, pcm_texts[idx])
    if not arg2_word_indices:
        df.at[idx, 'Arg2_RawTextPCM_Alignment'] = "Text Not Found"
    else:
        arg2_start, arg2_end = arg2_word_indices[0], arg2_word_indices[-1]
        pcm_indices_arg2 = get_aligned_indices(arg2_start, arg2_end, alignment_data[idx])
        if not pcm_indices_arg2:
            df.at[idx, 'Arg2_RawTextPCM_Alignment'] = "ALIGNMENT Error"
        else:
            df.at[idx, 'Arg2_RawTextPCM_Alignment'] = extract_words_from_indices(pcm_indices_arg2, pcm_texts[idx])
    connective = row['Connective_RawText']
    relation = row['Relation']
    if pd.isna(connective) or relation == "Implicit":  
        df.at[idx, 'Connective_RawTextPCM_Alignment'] = np.nan  
    else:
        connective_word_indices = get_word_indices_from_raw_text(connective, english_text)
        if not connective_word_indices:
            df.at[idx, 'Connective_RawTextPCM_Alignment'] = "Text Not Found"
        else:
            connective_start, connective_end = connective_word_indices[0], connective_word_indices[-1]
            pcm_indices_connective = get_aligned_indices(connective_start, connective_end, alignment_data[idx])
            if not pcm_indices_connective:
                df.at[idx, 'Connective_RawTextPCM_Alignment'] = "ALIGNMENT Error"
            else:
                df.at[idx, 'Connective_RawTextPCM_Alignment'] = extract_words_from_indices(pcm_indices_connective, pcm_texts[idx])
variants_df = pd.read_csv("/local/musaeed/NPIDRC/FullTransferMethod/variants.csv")
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
    if row['Connective_RawTextPCM_Alignment'] == "ALIGNMENT Error":
        connective_rawtext = row['Connective_RawText']
        variant1 = find_variant1(connective_rawtext)
        if variant1 is not None:
            df.at[idx, 'Connective_RawTextPCM_Alignment'] = variant1
current_date = datetime.now().strftime("%Y%m%d")
folder_path = f'/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/discontinous/projectedFiles/awesome/EnglishBERT/{current_date}'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
print(f"Folder '{folder_path}' has been created.")
arg1_raw_textPCM_alignment = df['Arg1_RawTextPCM_Alignment']
Arg2_RawTextPCM_Alignment = df['Arg2_RawTextPCM_Alignment']
connective_raw_textPCM_alignment = df['Connective_RawTextPCM_Alignment']  
ARG1_RawText = df['Arg1_RawText']
ARG2_RawText = df['Arg2_RawText']
English_Fulltext = df['FullRawText']
Relation = df['Relation']
PidginFullText = df['FullRawTextPCM']
combined_path = f'/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/discontinous/projectedFiles/awesome/EnglishBERT/{current_date}/combined'
value_counts = df['Connective_RawTextPCM_Alignment'].value_counts()
df.to_csv(f'{folder_path}/pdtb2_pcm_alignment_naijaLex_soft.csv', index=False)
combined_df = pd.DataFrame({
    'Arg1_RawTextPCM_Alignment': arg1_raw_textPCM_alignment,
    'Arg2_RawTextPCM_Alignment': Arg2_RawTextPCM_Alignment,
    'Connective_RawTextPCM_Alignment': connective_raw_textPCM_alignment,  
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
