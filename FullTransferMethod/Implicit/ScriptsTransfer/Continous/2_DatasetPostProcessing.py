import pandas as pd
df = pd.read_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/projectedDataset/Continous/PDTB2TranslatedData/local/musaeed/NPIDRC/FullTransferMethod/Implicit/projectedDataset/Continous/PDTB2TranslatedData.csv", low_memory=False)
df['FullRawText'] = df['FullRawTextPidginPostProcessed']
chars_to_strip = ' :,"|?()'
df['Arg1_Translated'] = df['Arg1_Translated'].str.strip().str.lstrip(chars_to_strip)
df['Arg2_Translated'] = df['Arg2_Translated'].str.strip().str.lstrip(chars_to_strip)
def get_start_index(span):
    return int(span.split('..')[0])
df['FullRawTextPidginContinous'] = df.apply(lambda row: row['Arg1_Translated'] + " " + row['Arg2_Translated']
                                            if get_start_index(row['Arg1_SpanList']) < get_start_index(row['Arg2_SpanList'])
                                            else row['Arg2_Translated'] + " " + row['Arg1_Translated'], axis=1)
print(df[['Arg1_Translated', 'Arg2_Translated', 'FullRawTextPidginContinous']].head())
df['Arg1_RawText']  = df['Arg1_Translated']
df['Arg2_RawText'] = df['Arg2_Translated']
df['FullRawText'] = df['FullRawTextPidginContinous']
df.to_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/projectedDataset/Continous/pdtb2ImplicitEntrelContinousProcessed.csv", index=False)