import pandas as pd
df_discontinous = pd.read_csv('/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/toBeMerged/awesome/pdtb2ImplicitEntrelDiscontiouswithoutSmoothing.csv', low_memory=False)
df_continous = pd.read_csv('/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Continous/pdtb2ImplicitEntrelContinousProcessed.csv', low_memory=False)
selected_columns = [
    "Relation", "Section", "FileNumber", "SentenceNumber", 
    "ConnHeadSemClass1", "ConnHeadSemClass2", 
    "Conn2SemClass1", "Conn2SemClass2", "Conn1", "Conn2",
    "Arg1_RawText", "Arg2_RawText", "Arg1_SpanList", "Arg2_SpanList", "FullRawText", "original_index"
]
df_continousSelect = df_continous[selected_columns]
df_discontinousSelect = df_discontinous[selected_columns]
df_merged = pd.merge(df_discontinousSelect, df_continousSelect, on="original_index", how='outer', suffixes=('_disc', '_cont'))
for col in selected_columns[:-1]:  
    df_merged[col] = df_merged[col + '_disc'].combine_first(df_merged[col + '_cont'])
for col in selected_columns[:-1]:  
    df_merged.drop([col + '_disc', col + '_cont'], axis=1, inplace=True)
df_merged_sorted = df_merged.sort_values(by='original_index')
df_merged_sorted.drop(columns=['original_index'], inplace=True)
print(df_merged_sorted.head())
df_merged_sorted.to_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Merged&Processed/awesome/pdtb2PidginImplicitEntrel.csv", index=False)
