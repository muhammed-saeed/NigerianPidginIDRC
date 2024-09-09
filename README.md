```markdown
# NigerianPidginIDRC

## Description

The work is about Implicit Discourse Relation classification for the Nigerian Pidgin language. Nigerian Pidgin is spoken by about 100 million people yet is considered a low-resource language. Our focus is on the discourse relation classification, particularly in the implicit setting.

Our two approaches are zeroshot and Cross Lingual Fine-Tuning. For the zeroshot approach, we start by training a state-of-the-art model in English using the following code:

We are performing 4-way and 11-way classification, and here are the sense levels we are using 

rels_11 = [
        "Comparison.Concession", "Comparison.Contrast",
        "Contingency.Cause", "Contingency.Pragmatic cause.Justification",
        "Expansion.Alternative", "Expansion.Conjunction", "Expansion.Instantiation", "Expansion.List", "Expansion.Restatement",
        "Temporal.Asynchronous", "Temporal.Synchrony"
    ]

rels_4 = ["Comparison", "Contingency", "Expansion", "Temporal"]


```python
CUDA_VISIBLE_DEVICES=6 python /PATH_TO/DiscoPrompt/DiscoPrompt.py \
--template_id 0 --max_steps 30000 \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-large \
--result_file PathToResults \
--ckpt_file englishBaseT5_v_1_large/DiscoPromptClassification_PDTB2 \
--prompt_lr 0.3 \
--project_root /PATH_TO/DiscoPrompt_REPO >PATH_TO_PRINT_OUTPUTenglishBaselineT5_v_1_1large/t5V1_1LargeLog.txt
```
You could change from `google\t5-v1_1-large` to the base version `google\t5-v1_1-base`
Then, we either test directly on the Pidgin dataset or we translate the Pidgin to English and test it using this code:

```python
CUDA_VISIBLE_DEVICES=1 python3 evaluate.py \
--csv_file_path "/PATH_TO_DATASET" \
--model_name_or_path 'google/t5-v1_1-base/large'  \
--eval_checkpoint "PATH_TO_CHECKPOINT" \
--template_id 0 \
--max_steps 30000 \
--batch_size 4 \
--eval_every_steps 250  \
--dataset ji  \
--prompt_lr 0.3 >> Path to PRINT THE LOG of the output
```

The other direction includes the creation of the Nigerian Pidgin NP Penn Discourse Treebank (NP-PDTB)-like dataset. To achieve the generation of the NP-PDTB, we first started by using an off-the-shelf translation model that needs this setup:

First one is using the \cite{lin2023low} "https://arxiv.org/abs/2307.00382" engine, from  then install the requirements and translate the English pdtb2 into Pidgin, 
```bash
pip install -r requirements.txt
```

Note we are using PDTB2 from this source `https://github.com/cgpotts/pdtb2` which contains csv file and we are translate the `FullRawText` column into Pidgin

```python
/PATH_TO/NigerianPidginIDRC/t5_translation/02_Translation.py
```

We trained two various models for translation (LLama and PL4MT).

For the LLama model  one needs the following setup:

```bash
git clone https://github.com/tloen/alpaca-lora
cd alpaca-lora
pip install -r requirments
```
Then train LLama Using
```
#Train
bash /PATH_TO/NigerianPidginIDRC/MachineTranslation/llama/train/finetune.sh
#Evaluate using 
bash /PATH_TO/NigerianPidginIDRC/MachineTranslation/llama/train/evaluatte.sh
```

and for the training with the PLM4MT First need the setup and then train:

```bash
pip install -r /PATH_TO/NigerianPidginIDRC/MachineTranslation/PLM4MT/requirments.txt
```
Data Preperation
```python
python/PATH_TO/NigerianPidginIDRC/MachineTranslation/PLM4MT/scripts/python/1_dataPreperation.py
bash /PATH_TO/NigerianPidginIDRC/MachineTranslation/PLM4MT/scripts/bash/train.sh
``` 

Our results have found that \cite{lin2023low} translation model is better than both the PLM4MT and the LLama2 and then we have used the \cite{lin2023low} model for our research

For the creation of the dataset, we have alignment-based and full transfer-based methods.

We also used various alignment models, including Awesome, SimAlign, GizaPy, PFT, and CRAFT.

The codes are organized in the 

```
/PATH_TO/NigerianPidginIDRC/AlignmentCenteric
/PATH_TO/NigerianPidginIDRC/FullTransferMethod
```

Then for the training of the DiscoPrompt Model the code
```
/PATH_TO/NigerianPidginIDRC/DiscoPromptPidgin
```

