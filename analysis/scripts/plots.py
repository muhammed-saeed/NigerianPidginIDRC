import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# File paths
files = [
    "BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAESimalignRobertaPidgin",
    "BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEAwesomeAlignFinetunedModel",
    "BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEAwesomeAlign",
    "BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAE",
    "BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEGiza"
]

# Base directory where the folders will be created
base_dir = "/PATH_TO/general-pidgin-modeling/analysis/figures/"

# Relation mapping for 4-way and 11-way classification
# [rel_map_4 and rel_map_11 as before]
rel_map_4 = defaultdict(lambda: -1, {
    "Comparison": 0,
    "Comparison.Concession": 0,
    "Comparison.Concession.Contra-expectation": 0,
    "Comparison.Concession.Expectation": 0,
    "Comparison.Contrast": 0,
    "Comparison.Contrast.Juxtaposition": 0,
    "Comparison.Contrast.Opposition": 0,
    "Comparison.Pragmatic concession": 0,
    "Comparison.Pragmatic contrast": 0,

    "Contingency": 1,
    "Contingency.Cause": 1,
    "Contingency.Cause.Reason": 1,
    "Contingency.Cause.Result": 1,
    "Contingency.Condition": 1,
    "Contingency.Condition.Hypothetical": 1,
    "Contingency.Pragmatic cause.Justification": 1,
    "Contingency.Pragmatic condition.Relevance": 1,

    "Expansion": 2,
    "Expansion.Alternative": 2,
    "Expansion.Alternative.Chosen alternative": 2,
    "Expansion.Alternative.Conjunctive": 2,
    "Expansion.Alternative.Disjunctive": 2,
    "Expansion.Conjunction": 2,
    "Expansion.Exception": 2,
    "Expansion.Instantiation": 2,
    "Expansion.List": 2,
    "Expansion.Restatement": 2,
    "Expansion.Restatement.Equivalence": 2,
    "Expansion.Restatement.Generalization": 2,
    "Expansion.Restatement.Specification": 2,

    "Temporal": 3,
    "Temporal.Asynchronous.Precedence": 3,
    "Temporal.Asynchronous.Succession": 3,
    "Temporal.Synchrony": 3})

# Relation mapping for 11-way classification
rel_map_11 = defaultdict(lambda: -1, {
        # "Comparison",
        "Comparison.Concession": 0,
        "Comparison.Concession.Contra-expectation": 0,
        "Comparison.Concession.Expectation": 0,
        "Comparison.Contrast": 1,
        "Comparison.Contrast.Juxtaposition": 1,
        "Comparison.Contrast.Opposition": 1,
        # "Comparison.Pragmatic concession",
        # "Comparison.Pragmatic contrast",

        # "Contingency",
        "Contingency.Cause": 2,
        "Contingency.Cause.Reason": 2,
        "Contingency.Cause.Result": 2,
        "Contingency.Pragmatic cause.Justification": 3,
        # "Contingency.Condition",
        # "Contingency.Condition.Hypothetical",
        # "Contingency.Pragmatic condition.Relevance",

        # "Expansion",
        "Expansion.Alternative": 4,
        "Expansion.Alternative.Chosen alternative": 4,
        "Expansion.Alternative.Conjunctive": 4,
        "Expansion.Conjunction": 5,
        "Expansion.Instantiation": 6,
        "Expansion.List": 7,
        "Expansion.Restatement": 8,
        "Expansion.Restatement.Equivalence": 8,
        "Expansion.Restatement.Generalization": 8,
        "Expansion.Restatement.Specification": 8,
        # "Expansion.Alternative.Disjunctive",
        # "Expansion.Exception",

        # "Temporal",
        "Temporal.Asynchronous.Precedence": 9,
        "Temporal.Asynchronous.Succession": 9,
        "Temporal.Synchrony": 10})


# Function to map and count occurrences
def map_and_count(df, rel_map):
    df['MappedClass'] = df['ConnHeadSemClass1'].map(rel_map)
    return df['MappedClass'].value_counts()

# Plotting function
def plot_counts(counts, title, file_path, classification_type):
    counts = counts.sort_index()
    fig, ax = plt.subplots()
    counts.plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Class')
    ax.set_ylabel('Number of Annotations')
    
    # Create the directory for the dataset if it doesn't exist
    dataset_folder = os.path.join(base_dir, os.path.basename(file_path))
    os.makedirs(dataset_folder, exist_ok=True)
    
    # Save the figure
    fig.savefig(os.path.join(dataset_folder, f"{classification_type}_classification.png"))

# Process each file
for file_name in files:
    # Correct the file path by adding the appropriate subdirectory and file extension
    file_path = os.path.join(f"{file_name}.csv")  # This should be the correct path to your CSV files
    
    # Check if the file exists before proceeding
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        continue
    
    # Load data
    df = pd.read_csv(file_path, low_memory=False)

    # Filter data for implicit relations in specified sections
    df_filtered = df[(df["Relation"] == "Implicit") & (df["Section"].isin([21, 22]))]

    # Map and count for 4-way classification
    counts_4_way = map_and_count(df_filtered.copy(), rel_map_4)
    print(counts_4_way)
    plot_counts(counts_4_way, f"4-way Classification for {file_name}", file_name, "4_way")  # Pass file_name instead of file_path

    # Map and count for 11-way classification
    counts_11_way = map_and_count(df_filtered.copy(), rel_map_11)
    print(counts_11_way)
    plot_counts(counts_11_way, f"11-way Classification for {file_name}", file_name, "11_way")  # Pass file_name instead of file_path
