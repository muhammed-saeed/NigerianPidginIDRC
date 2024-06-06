import pandas as pd
import numpy as np


file_path = "/local/musaeed/NPIDRC/NaijaDiscoDataset/dataset/annotations_final_with_utt_withPidgin.csv"
df = pd.read_csv(file_path)


pdtb_mapping = {
    "Temporal.Synchronous": "Temporal.Synchronous",
    "Temporal.Asynchronous.Precedence": "Temporal.Asynchronous.Precedence",
    "Temporal.Asynchronous.Succession": "Temporal.Asynchronous.Succession",
    "Contingency.Cause.Reason": "Contingency.Cause.Reason",
    "Contingency.Cause.Result": "Contingency.Cause.Result",
    "Contingency.Cause.NegResult": None,
    "Contingency.Cause+Belief.Reason+Belief": "Contingency.PragmaticCause",
    "Contingency.Cause+Belief.Result+Belief": "Contingency.PragmaticCause",
    "Contingency.Cause+SpeechAct.Reason+SpeechAct": "Contingency.Cause.Reason",
    "Contingency.Cause+SpeechAct.Result+SpeechAct": "Contingency.Cause.Result",
    "Contingency.Purpose.Arg-1-as-goal": "Contingency.Cause.Result",
    "Contingency.Purpose.Arg-2-as-goal": None,
    "Contingency.Condition.Arg1-as-condition": "Contingency.Condition",
    "Contingency.Condition.Arg2-as-condition": "Contingency.Condition",
    "Contingency.Condition+SpeechAct": "Contingency.PragmaticCondition",
    "Contingency.NegativeCondition.Arg1-as-Negcondition": None,
    "Contingency.NegativeCondition.Arg2-as-Negcondition": "Expansion.Alternative.Disjunctive",
    "Comparison.Contrast": "Comparison.Contrast",
    "Comparison.Similarity": "Expansion.Conjunction",
    "Comparison.Concession.Arg-1-as-denier": "Comparison.Concession.Expectation",
    "Comparison.Concession.Arg-2-as-denier": "Comparison.Concession.ContraExpectation",
    "Comparison.Concession+SpeechAct": "Comparison.Concession.ContraExpectation",
    "Expansion.Conjunction": "Expansion.Conjunction",
    "Expansion.Disjunction": "Expansion.Alternative.Disjunctive",
    "Expansion.Level-of-detail.Arg2-as-detail": "Expansion.Restatement.Specification",
    "Expansion.Level-of-detail.Arg1-as-detail": "Expansion.Restatement.Generalization",
    "Expansion.Equivalence": "Expansion.Restatement.Equivalence",
    "Expansion.Instantiation.Arg2-as-instance": "Expansion.Instantiation",
    "Expansion.Instantiation.Arg1-as-instance": None,
    "Expansion.Exception.Arg1-as-except": "Expansion.Exception",
    "Expansion.Exception.Arg2-as-except": "Expansion.Exception",
    "Expansion.Substitution.Arg1-as-subst": None,
    "Expansion.Substitution.Arg2-as-subst": "Expansion.Alternative.ChosenAlternative",
    "Expansion.Manner.Arg1-as-manner": None,
    "Expansion.Manner.Arg2-as-manner": None
}


def apply_mapping(value):
    if pd.isna(value) or value not in pdtb_mapping:
        return None
    return pdtb_mapping.get(value)

df['NP_rs1_mapped'] = df['NP_rs1'].apply(apply_mapping)
df['NP_rs2_mapped'] = df['NP_rs2'].apply(apply_mapping)

print(df[['NP_rs1', 'NP_rs1_mapped', 'NP_rs2', 'NP_rs2_mapped']].head())
dfImpEnt = df[(df["reltype"]=="Implicit")|(df["reltype"]=="EntRel")]
print(dfImpEnt.NP_rs1.value_counts())
print(dfImpEnt.NP_rs1_mapped.value_counts())

print(dfImpEnt.NP_rs2.value_counts())
print(dfImpEnt.NP_rs2_mapped.value_counts())

def extract_first_span_start(span):
    if pd.isna(span):
        return float('inf')  
    first_span = span.split(';')[0]  
    start = first_span.split('..')[0]
    return int(start)


def apply_fullrawtext_logic(df):
    df['Arg1_FirstSpanStart'] = df['NP_arg1_utt_span'].apply(extract_first_span_start)
    df['Arg2_FirstSpanStart'] = df['NP_arg2_utt_span'].apply(extract_first_span_start)
    
    full_text_list = []
    
    for index, row in df.iterrows():
        arg1_text = row['NP_arg1_utt'] if pd.notna(row['NP_arg1_utt']) else ""
        arg2_text = row['NP_arg2_utt'] if pd.notna(row['NP_arg2_utt']) else ""
        if row['Arg1_FirstSpanStart'] < row['Arg2_FirstSpanStart']:
            full_text = arg1_text + " " + arg2_text
        else:
            full_text = arg2_text + " " + arg1_text
        full_text_list.append(full_text)
    
    
    df['FullRawText'] = full_text_list
    return df


dfImpEnt = apply_fullrawtext_logic(dfImpEnt)

RealPidgin = {
    'NP_reltype':"Relation",
    "NP_arg1_utt":"Arg1_RawText",
    "NP_arg2_utt":"Arg2_RawText",
    "NP_conn1": "Conn1",
    "NP_conn2": "Conn2",
    "NP_rs1_mapped": "ConnHeadSemClass1",
    "NP_rs2_mapped": "Conn2SemClass1",
    "NP_arg1_utt_span": "Arg1_SpanList",
    "NP_arg2_utt_span": "Arg2_SpanList",
}


dfImpEnt = dfImpEnt.rename(columns=RealPidgin)
dfImpEnt['FileNumber'] = dfImpEnt.index
dfImpEnt['Section'] = 22
dfImpEnt["Conn2SemClass2"] = np.NaN
dfImpEnt["ConnHeadSemClass2"] = np.NaN





dfImpEnt.to_csv("/local/musaeed/NPIDRC/NaijaDiscoDataset/dataset/Mapped/mappedSenses/ImplicitEntrelRealPidginDiscoPromptToEval.csv", index=False)




def apply_fullrawtext_logic(df):
    
    df['Arg1_FirstSpanStart'] = df['Arg1_SpanList'].apply(extract_first_span_start)
    df['Arg2_FirstSpanStart'] = df['Arg2_SpanList'].apply(extract_first_span_start)
    
    
    full_text_list = []
    
    
    for index, row in df.iterrows():
        arg1_text = row['Arg1English_Translated'] if pd.notna(row['Arg1English_Translated']) else ""
        arg2_text = row['Arg2English_Translated'] if pd.notna(row['Arg2English_Translated']) else ""
        if row['Arg1_FirstSpanStart'] < row['Arg2_FirstSpanStart']:
            full_text = arg1_text + " " + arg2_text
        else:
            full_text = arg2_text + " " + arg1_text
        full_text_list.append(full_text)
    
    
    df['FullRawText'] = full_text_list
    return df



file_path = "/local/musaeed/NPIDRC/NaijaDiscoDataset/dataset/translatedToEnglish/NaijaDiscoTranslatedData.csv"
dfEN = pd.read_csv(file_path)
dfEN['NP_rs1'] = dfEN['ConnHeadSemClass1']
dfEN['NP_rs2'] = dfEN['Conn2SemClass1']
print(dfEN.ConnHeadSemClass1.value_counts())
print(dfEN.Conn2SemClass1.value_counts())

dfEN['ConnHeadSemClass1_mapped'] = np.nan
dfEN['Conn2SemClass1_mapped'] = np.nan


dfEN['NP_rs1_mapped'] = dfEN['NP_rs1'].apply(apply_mapping)
dfEN['NP_rs2_mapped'] = dfEN['NP_rs2'].apply(apply_mapping)


print(dfEN[['NP_rs1', 'NP_rs1_mapped', 'NP_rs2', 'NP_rs2_mapped']].head())
dfENImpEnt = dfEN[(dfEN["reltype"]=="Implicit")|(dfEN["reltype"]=="EntRel")]
print(dfENImpEnt.NP_rs1.value_counts())
print(dfENImpEnt.NP_rs1_mapped.value_counts())

print(dfENImpEnt.NP_rs2.value_counts())
print(dfENImpEnt.NP_rs2_mapped.value_counts())


dfENImpEnt = apply_fullrawtext_logic(dfENImpEnt)


TranslatePidgin = {
    'NP_reltype':"Relation",
    "Arg1English_Translated":"Arg1_RawText",
    "Arg2English_Translated":"Arg2_RawText",
    "NP_conn1": "Conn1",
    "NP_conn2": "Conn2",
    "ConnHeadSemClass1_mapped": "ConnHeadSemClass1",
    "Conn2SemClass1_mapped": "Conn2SemClass1",
    "NP_arg1_utt_span": "Arg1_SpanList",
    "NP_arg2_utt_span": "Arg2_SpanList",
}

dfENImpEnt = dfENImpEnt.rename(columns=TranslatePidgin)
dfENImpEnt['FileNumber'] = dfENImpEnt.index
dfENImpEnt['Section'] = 22
dfENImpEnt["Conn2SemClass2"] = np.NaN
dfENImpEnt["ConnHeadSemClass2"] = np.NaN





dfENImpEnt.to_csv("/local/musaeed/NPIDRC/NaijaDiscoDataset/dataset/Mapped/mappedSenses/TranslatedPidginToEnglishImplicitEntRelDiscoPromptToEval.csv", index=False)


