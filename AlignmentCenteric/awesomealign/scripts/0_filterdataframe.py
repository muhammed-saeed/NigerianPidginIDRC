import pandas as pd
df = pd.read_csv('pdtb2_pcm.csv', low_memory=False)
english = df["FullRawText"].to_list()
pcm = df["FullRawText_PCM"].to_list()
with open('/local/musaeed/NPIDRC/align/simAlgin/twiceTEst/english.txt', 'w', encoding='utf-8') as english_file:
    for text in english:
        english_file.write(text + '\n')
with open('/local/musaeed/NPIDRC/align/simAlgin/twiceTEst/pcm.txt', 'w', encoding='utf-8') as pcm_file:
    for text in pcm:
        pcm_file.write(text + '\n')
