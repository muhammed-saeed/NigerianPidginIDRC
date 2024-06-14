import pandas as pd
df_main = pd.read_csv("/PATH_TO/NPIDRC/PDTB2/dataset/pdtb2TranslatedPostProcessing.csv", low_memory=False)
df_discountinous = pd.read_csv("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/DisContinousImplicitpdtb2ExtractedWithPostProecessingTranslation.csv", low_memory=False)
df_main['original_index'] = df_main.index  
df_discountinous.rename(columns={'orignal_index': 'original_index'}, inplace=True)
with open("/PATH_TO/NPIDRC/FullTransferMethod/FinalPDTBDataSet/PCM2EnglishPDTB.txt", 'r') as file:
    alignmentsText = file.readlines()
with open("/PATH_TO/NPIDRC/align/awesomealign/data/extractedAlignmentUsingEnglishBERT.txt", "r") as fb:
    alignments = fb.readlines()
filtered_alignmentsText = [alignmentsText[idx] for idx in df_discountinous['original_index']]
filtered_alignments = [alignments[idx] for idx in df_discountinous['original_index']]
with open("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/awesome/englishBERTAlignment/EnglishBERTfiltered_alignmentsText.txt", 'w') as f:
    f.writelines(filtered_alignmentsText)
with open("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/awesome/englishBERTAlignment/EnglishBERTfiltered_alignmentsPCM2EN.txt", 'w') as f:
    f.writelines(filtered_alignments)
english_fullRawtext = [sent + "\n" for sent in df_discountinous['FullRawTextExtracted'].tolist()]
pidgin_fullRawtext = [sent + "\n" for sent in df_discountinous['FullRawTextPidginPostProcessed'].tolist()]  
with open("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/awesome/englishBERTAlignment/EnglishBERTDiscontinousImpEntrelenglish.txt", "w") as fb:
    fb.writelines(english_fullRawtext)
with open("/PATH_TO/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/textfiles/awesome/englishBERTAlignment/EnglishBERTDiscontinousImpEntrelpidgin.txt", "w") as fb:
    fb.writelines(pidgin_fullRawtext)
