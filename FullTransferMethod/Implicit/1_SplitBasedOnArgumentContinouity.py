import pandas as pd


main_df = pd.read_csv("/local/musaeed/NPIDRC/PDTB2/dataset/pdtb2TranslatedPostProcessing.csv", low_memory=False)


df = main_df[(main_df['Relation'] == "Implicit") | (main_df['Relation'] == "EntRel")]


df['original_index'] = df.index


def is_continuous(row):
    
    columns_to_check = ['Arg1_SpanList', 'Arg2_SpanList', 'Connective_SpanList']
    
    for col in columns_to_check:
        if ';' in str(row[col]):
            return False
    return True


df['is_continuous'] = df.apply(is_continuous, axis=1)


df_continuous = df[df['is_continuous']]
df_discontinuous = df[~df['is_continuous']]


df_continuous.to_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ContinousImplicitpdtb2ExtractedWithPostProecessingTranslation.csv", index=False)
df_discontinuous.to_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/DisContinousImplicitpdtb2ExtractedWithPostProecessingTranslation.csv", index=False)







print(f'The length of continous dataframe is {len(df_continuous)}')
print(f"The length of the discountinous dataframe is {len(df_discontinuous)}")
