import pandas as pd
from tqdm import tqdm
from simalign import SentenceAligner
df_main = pd.read_csv("/PATH_TO/NPIDRC/PDTB2/dataset/pdtb2TranslatedPostProcessing.csv", low_memory=False)
df_discountinous = pd.read_csv("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/DisContinousImplicitpdtb2ExtractedWithPostProecessingTranslation.csv", low_memory=False)
df_main['original_index'] = df_main.index  
df_discountinous.rename(columns={'orignal_index': 'original_index'}, inplace=True)
english_fullRawtext = [sent + "\n" for sent in df_discountinous['FullRawTextExtracted'].tolist()]
pidgin_fullRawtext = [sent + "\n" for sent in df_discountinous['FullRawTextPidginPostProcessed'].tolist()]
with open("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/simalign/DiscontinousImpEntrelenglish.txt", "w") as fb:
    fb.writelines(english_fullRawtext)
with open("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/simalign/DiscontinousImpEntrelpidgin.txt", "w") as fb:
    fb.writelines(pidgin_fullRawtext)
myaligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")
alignments_list = []
total_sentences = len(pidgin_fullRawtext)
with tqdm(total=total_sentences, desc="Aligning sentences") as pbar:
    for pcm_sent, english_sent in zip(pidgin_fullRawtext, english_fullRawtext):
        alignments = myaligner.get_word_aligns(pcm_sent.split(), english_sent.split())
        alignment_pairs = alignments["mwmf"]
        formatted_alignments = [f"{src_idx}-{trg_idx}" for src_idx, trg_idx in alignment_pairs]
        formatted_output = " ".join(formatted_alignments)
        alignments_list.append(formatted_output)
        pbar.update(1)  
with open("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/simalign/filtered_alignmentsEN2PCM.txt", "w", encoding="utf-8") as f:
    for alignment in alignments_list:
        f.write(f"{alignment}\n")
