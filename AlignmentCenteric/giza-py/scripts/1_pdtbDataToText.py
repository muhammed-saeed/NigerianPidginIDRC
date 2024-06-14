import pandas as pd
df = pd.read_csv("/PATH_TO/pdtb2_pcm.csv", low_memory=False)
pcmRawText = df['FullRawText_PCM'].tolist()
enRawText = df['FullRawText'].tolist()
print(f"length {len(pcmRawText)} and length {len(enRawText)}")
with open("/PATH_TO/NPIDRC/giza-py/pdtbText/en.txt", "w") as fb:
    for line in enRawText:
        fb.write(line + '\n')
with open("/PATH_TO/NPIDRC/giza-py/pdtbText/pcm.txt", "w") as fb:
    for line in pcmRawText:
        fb.write(line + '\n')
