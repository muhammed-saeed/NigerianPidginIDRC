import pandas as pd
from simpletransformers.t5 import T5Model, T5Args


model_args = T5Args()
model_args.max_length = 192
model_args.length_penalty = 1
model_args.num_beams = 5
model_args.evaluation_batch_size = 16


model_output_dir = "/local/musaeed/BESTT5TranslationModel"
model = T5Model("t5", model_output_dir, args=model_args, use_cuda=False)


df = pd.read_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ContinousImplicitpdtb2ExtractedWithPostProecessingTranslation.csv", low_memory=False)


def prepare_translation(texts):
    translations = []
    indices = []
    for i, text in enumerate(texts):
        if pd.notna(text):
            translations.append("translate English to pcm: " + text)
            indices.append(i)
    return translations, indices


Arg1_texts, Arg1_indices = prepare_translation(df['Arg1_RawTextExtracted'])
Arg2_texts, Arg2_indices = prepare_translation(df['Arg2_RawTextExtracted'])


Arg1_translated = model.predict(Arg1_texts)
Arg2_translated = model.predict(Arg2_texts)


def reinsert_translations(original_list, translations, indices):
    translated_full = ['NaN'] * len(original_list)
    for i, idx in enumerate(indices):
        translated_full[idx] = translations[i]
    return translated_full


df['Arg1_Translated'] = reinsert_translations(df['Arg1_RawTextExtracted'], Arg1_translated, Arg1_indices)
df['Arg2_Translated'] = reinsert_translations(df['Arg2_RawTextExtracted'], Arg2_translated, Arg2_indices)


df.to_csv("/local/musaeed/NPIDRC/FullTransferMethod/Implicit/projectedDataset/PDTB2TranslatedData.csv", index=False)
