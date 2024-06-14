```markdown
# NigerianPidginIDRC

## Description

The work is about Implicit Discourse Relation classification for the Nigerian Pidgin language. Nigerian Pidgin is spoken by about 100 million people yet is considered a low-resource language. Our focus is on the discourse relation classification, particularly in the implicit setting.

Our two approaches are zeroshot and Cross Lingual Fine-Tuning. For the zeroshot approach, we start by training a state-of-the-art model in English using the following code:


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

First one is using the \cite{lin23low} engine, from  then install the requirements and translate the English pdtb2 into Pidgin, 
```bash
pip install -r requirements.txt
```

Note we are using PDTB2 from this source `https://github.com/cgpotts/pdtb2` which contains csv file and we are translate the `FullRawText` column into Pidgin

```python
/PATH_TO/NigerianPidginIDRC/t5_translation/02_Translation.py
```

We trained two various models for translation.

The first one needs the following setup:

```bash
pip install -r requirments
```

and then train with:

```python
# Training code
``` 

For the creation of the dataset, we have alignment-based and full transfer-based methods.

We also used various alignment models, including Awesome, SimAlign, GizaPy, PFT, and CRAFT.
```

