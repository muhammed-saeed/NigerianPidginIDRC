import pandas as pd


def count_implicit(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    implicit_count = df[df["Relation"] == "Implicit"].shape[0]
    return implicit_count


awesome_file = "/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Merged&Processed/awesome/pdtb2PidginImplicitEntrel.csv"
giza_file = "/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Merged&Processed/gizapy/pdtb2PidginImplicitEntrel.csv"
pft_file = "/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Merged&Processed/pft/pdtb2PidginImplicitEntrel.csv"
simAlign_file = "/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Merged&Processed/simAlign/pdtb2PidginImplicitEntrel.csv"
cat_file = "/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Merged&Processed/simAlignRoBERTa/pdtb2PidginImplicitEntrel.csv"


awesome_count = count_implicit(awesome_file)
giza_count = count_implicit(giza_file)
pft_count = count_implicit(pft_file)
simAlign_count = count_implicit(simAlign_file)
cat_count = count_implicit(cat_file)


print("Number of Implicit instances in 'awesome':", awesome_count)
print("Number of Implicit instances in 'giza':", giza_count)
print("Number of Implicit instances in 'pft':", pft_count)
print("Number of Implicit instances in 'simAlign':", simAlign_count)
print("Number of Implicit instances in 'cat':", cat_count)
