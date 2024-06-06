import pandas as pd
df = pd.read_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/ScriptsTransfer/DisContinous/simAlignRoBERTa/data/ModifiedMain.csv", low_memory=False)
df['Arg1_RawText'] = df['Arg1_RawTextPCM_Alignment']
df['Arg2_RawText'] = df['Arg2_RawTextPCM_Alignment']
df['FullRawText'] = df['FullRawTextPidginPostProcessed']
df.to_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/discontinous/toBeMerged/pft/pdtb2ImplicitEntrelDiscontiouswithoutSmoothing.csv", index=False)
