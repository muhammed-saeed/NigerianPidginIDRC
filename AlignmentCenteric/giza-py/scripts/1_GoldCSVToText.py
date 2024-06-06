import pandas as pd
df = pd.read_csv('/local/musaeed/NPIDRC/data/trainDatawithoutDevNorTest.tsv',sep="\t").astype(str)
filtered_df = df[df['prefix'] == 'translate english to pcm']
input_texts = filtered_df['input_text'].tolist()
target_texts = filtered_df['target_text'].tolist()
with open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/textFiles/english.txt", "w") as file:
    for text in input_texts:
        file.write(str(text) + "\n")
with open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/textFiles/pcm.txt", "w") as file:
    for text in target_texts:
        file.write(str(text) + "\n")
