import pandas as pd

df = pd.read_csv("/PATH_TO/DRCNP/align/awesomealign/data/TextError/FineTunedModel/20240305/pdtb2_pcm_alignment_naijaLex_soft.csv", low_memory=False)
import pandas as pd

# Assuming df is your DataFrame

# Check and handle alignment errors for arg1_rawTextPCM_alignment
df['arg1_rawTextPCM_alignment'] = df['arg1_rawTextPCM_alignment'].apply(lambda x: 'alignment error' if x == 'alignment error' else 'text not found' if x == 'text not found' else x)

# Check and handle alignment errors for arg2_raw_textPCM_alignment
df['arg2_raw_textPCM_alignment'] = df['arg2_raw_textPCM_alignment'].apply(lambda x: 'alignment error' if x == 'alignment error' else 'text not found' if x == 'text not found' else x)

# Check and handle alignment errors for connective_rawTextPCM_alignment
df['connective_rawTextPCM_alignment'] = df['connective_rawTextPCM_alignment'].apply(lambda x: 'alignment error' if x == 'alignment error' else 'text not found' if x == 'text not found' else x)

# Print the values
print(f"{df.arg1_rawTextPCM_alignment}")
print(f"{df.arg2_raw_textPCM_alignment}")
print(f"{df.connective_rawTextPCM_alignment}")
