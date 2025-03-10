from openprompt import PromptDataLoader
from openprompt.prompts import ManualVerbalizer
from openprompt.prompts import SoftTemplate, MixedTemplate
from openprompt import PromptForClassification
from openprompt.data_utils.data_sampler import FewShotSampler


from openprompt.utils.logging import logger

import pandas as pd
from tqdm import tqdm
import torch
import argparse
import numpy as np
import time
import os
import re
import json
import math


from openprompt.utils.reproduciblity import set_seed
from openprompt.plms import load_plm
from transformers import AdamW, get_linear_schedule_with_warmup,get_constant_schedule_with_warmup
from transformers.optimization import Adafactor, AdafactorSchedule  

from data_utils import PDTB2Processor, PDTB3Processor, CoNLL15Processor
from utils import evaluate
from openprompt.prompts import PTRTemplate
from discoverbalizer import DiscoVerbalizer

parser = argparse.ArgumentParser("")
parser.add_argument("--seed", type=int, default=144)
parser.add_argument("--plm_eval_mode", action="store_true", help="whether to turn off the dropout in the freezed model. Set to true to turn off.")
parser.add_argument("--tune_plm", action="store_true", help="Whether to tune the plm, default to False")
parser.add_argument("--few_shot", action="store_true", help="Whether to tune the plm, default to False")
parser.add_argument("--shot", type=int, default=-1)
parser.add_argument("--few_shot_data",  type=str, default="./DiscoPrompt/PDTB2-Imp-Fewshot")

parser.add_argument("--model", type=str, default='t5', help="We test both t5 in this scripts, the corresponding tokenizerwrapper will be automatically loaded.")
parser.add_argument("--model_name_or_path", default='/model_path/t5-base')
parser.add_argument("--project_root", default='/', help="The project root in the file system")
parser.add_argument("--template_file", default='DiscoPropmt_template.txt', help="The project root in the file system")                    
parser.add_argument("--template_id", type=int, default=0)
parser.add_argument("--verbalizer_id", type=int, default=0)

parser.add_argument("--dataset",type=str, default= "ji" )
parser.add_argument("--result_file", type=str, default="./DiscoPrompt/results/results.txt")
parser.add_argument("--ckpt_file", type=str, default="DiscoPromptClassification_results")
parser.add_argument("--eval_checkpoint", type=str, default="DiscoPromptClassification_results")

parser.add_argument("--num_classes", default=11, type=int)
parser.add_argument("--max_steps", default=30000, type=int)
parser.add_argument("--max_seq_length", default=350, type=int)
parser.add_argument("--prompt_lr", type=float, default=0.3)
parser.add_argument("--batch_size", type=int, default=4)
parser.add_argument("--batch_size_e", type=int, default=4)
parser.add_argument("--eval_every_steps", type=int, default=250)

parser.add_argument("--dataset_decoder_max_length", default=50, type=int)
parser.add_argument("--decoder_max_length", default=10, type=int)
parser.add_argument("--gradient_accumulation_steps", default=4, type=int)
parser.add_argument("--soft_token_num", type=int, default=20)
parser.add_argument("--optimizer", type=str, default="Adafactor")
parser.add_argument("--warmup_step_prompt", type=int, default=0)
parser.add_argument("--init_from_vocab", action="store_false")
args = parser.parse_args()

content_write = "="*20+"\n"
content_write += f"dataset {args.dataset}\t"
content_write += f"temp_file {args.template_file}\t"                 
content_write += f"temp {args.template_id}\t"
content_write += f"verb {args.verbalizer_id}\t"
content_write += f"model {args.model_name_or_path}\t"
content_write += f"seed {args.seed}\t"
content_write += f"few_shot {args.few_shot}\t"
content_write += f"shot {args.shot}\t"
content_write += f"max_steps {args.max_steps}\t"
content_write += f"eval_every_steps {args.eval_every_steps}\t"
content_write += f"prompt_lr {args.prompt_lr}\t"
content_write += f"batch_size {args.batch_size}\t"
content_write += f"optimizer {args.optimizer}\t"
content_write += f"ckpt_file {args.ckpt_file}\t"
content_write += "\n"
print(content_write)

if args.dataset == "ji":      
    num_classes = 11 
    Processor = PDTB2Processor(num_labels=num_classes)
    
    data_dir = "/PATH_TO/DiscoPrompt/PDTB2-Imp"
    
    
    pdtb2_df = pd.read_csv("/PATH_TO/pdtb2_english.csv", low_memory=False)

    
    train_sections = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    valid_sections = [0,1]
    test_sections = [21,22]

    
    pdtb2_df['label'] = None
    pdtb2_df.loc[pdtb2_df['Section'].isin(train_sections), 'label'] = 'train'
    pdtb2_df.loc[pdtb2_df['Section'].isin(valid_sections), 'label'] = 'valid'
    pdtb2_df.loc[pdtb2_df['Section'].isin(test_sections), 'label'] = 'test'

    
    train_df = pdtb2_df[pdtb2_df['label'] == 'train']
    valid_df = pdtb2_df[pdtb2_df['label'] == 'valid']
    test_df = pdtb2_df[pdtb2_df['label'] == 'test']

    
    dataset = {}
    dataset['train'] = Processor.get_examples(train_df, 'train')
    dataset['validation'] = Processor.get_examples(valid_df, 'dev')
    dataset['test'] = Processor.get_examples(test_df, 'test')
    

    class_labels = Processor.get_labels()
    label_words = {
    "Comparison.Concession"  :["if", "Comparison", "Concession"],
    "Comparison.Contrast"    :["however", "Comparison", "Contrast"],
    "Contingency.Cause"      :["so", "Contingency", "Cause"],
    "Contingency.Pragmatic cause.Justification"  :["indeed", "Contingency", "Pragmatic"],
    "Expansion.Alternative"  :["instead", "Expansion", "Alternative"],
    "Expansion.Conjunction"  :["also", "Expansion", "Conjunction"],
    "Expansion.Instantiation":["for", "Expansion", "Instantiation"],
    "Expansion.List"         :["and", "Expansion", "List"],
    "Expansion.Restatement"  :["specifically", "Expansion", "Restatement"],
    "Temporal.Asynchronous"  :["before", "Temporal", "Asynchronous"],
    "Temporal.Synchrony"     :["when", "Temporal", "Synchrony"],
    }

elif args.dataset == "ji-2class":      
    num_classes = 11 
    Processor = PDTB2Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/PDTB2-Imp"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'test')
    class_labels = Processor.get_labels()
    label_words = {
    "Comparison.Concession"  :["Comparison", "Concession"],
    "Comparison.Contrast"    :["Comparison", "Contrast"],
    "Contingency.Cause"      :["Contingency", "Cause"],
    "Contingency.Pragmatic cause.Justification"  :["Contingency", "Pragmatic"],
    "Expansion.Alternative"  :["Expansion", "Alternative"],
    "Expansion.Conjunction"  :["Expansion", "Conjunction"],
    "Expansion.Instantiation":["Expansion", "Instantiation"],
    "Expansion.List"         :["Expansion", "List"],
    "Expansion.Restatement"  :["Expansion", "Restatement"],
    "Temporal.Asynchronous"  :["Temporal", "Asynchronous"],
    "Temporal.Synchrony"     :["Temporal", "Synchrony"],
    }

elif args.dataset == "ji-topcon":      
    num_classes = 11 
    Processor = PDTB2Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/PDTB2-Imp"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    if args.few_shot: 
        train_data_dir = args.few_shot_data
        dataset['train'] = Processor.get_examples(train_data_dir, 'train') 
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'test')
    class_labels = Processor.get_labels()
    label_words = {
    "Comparison.Concession"  :["if", "Comparison"],
    "Comparison.Contrast"    :["however", "Comparison"],
    "Contingency.Cause"      :["so", "Contingency"],
    "Contingency.Pragmatic cause.Justification"  :["indeed", "Contingency"],
    "Expansion.Alternative"  :["instead", "Expansion"],
    "Expansion.Conjunction"  :["also", "Expansion"],
    "Expansion.Instantiation":["for", "Expansion"],
    "Expansion.List"         :["and", "Expansion"],
    "Expansion.Restatement"  :["specifically", "Expansion"],
    "Temporal.Asynchronous"  :["before", "Temporal"],
    "Temporal.Synchrony"     :["when", "Temporal"],
    }

elif args.dataset == "ji-seccon":      
    num_classes = 11 
    Processor = PDTB2Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/PDTB2-Imp"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'test')
    class_labels = Processor.get_labels()
    label_words = {
    "Comparison.Concession"  :["if", "Concession"],
    "Comparison.Contrast"    :["however", "Contrast"],
    "Contingency.Cause"      :["so", "Cause"],
    "Contingency.Pragmatic cause.Justification"  :["indeed", "Pragmatic"],
    "Expansion.Alternative"  :["instead", "Alternative"],
    "Expansion.Conjunction"  :["also", "Conjunction"],
    "Expansion.Instantiation":["for", "Instantiation"],
    "Expansion.List"         :["and", "List"],
    "Expansion.Restatement"  :["specifically", "Restatement"],
    "Temporal.Asynchronous"  :["before", "Asynchronous"],
    "Temporal.Synchrony"     :["when", "Synchrony"],
    }

elif args.dataset == "ji-connectiveonly":      
    num_classes = 11 
    Processor = PDTB2Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/PDTB2-Imp"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    if args.few_shot: 
        train_data_dir = args.few_shot_data
        dataset['train'] = Processor.get_examples(train_data_dir, 'train') 
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'test')
    class_labels = Processor.get_labels()
    label_words = {
    "Comparison.Concession"  :["if"],
    "Comparison.Contrast"    :["however"],
    "Contingency.Cause"      :["so"],
    "Contingency.Pragmatic cause.Justification"  :["indeed"],
    "Expansion.Alternative"  :["instead"],
    "Expansion.Conjunction"  :["also"],
    "Expansion.Instantiation":["for"],
    "Expansion.List"         :["and"],
    "Expansion.Restatement"  :["specifically"],
    "Temporal.Asynchronous"  :["before"],
    "Temporal.Synchrony"     :["when"],
    }
    



    




















elif args.dataset == "lin":      
    num_classes = 11 
    Processor = PDTB2Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/PDTB2-Imp-Lin"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'test')
    class_labels = Processor.get_labels()
    label_words = {
    "Comparison.Concession"  :["if", "Comparison", "Concession"],
    "Comparison.Contrast"    :["however", "Comparison", "Contrast"],
    "Contingency.Cause"      :["so", "Contingency", "Cause"],
    "Contingency.Pragmatic cause.Justification"  :["indeed", "Contingency", "Pragmatic"],
    "Expansion.Alternative"  :["instead", "Expansion", "Alternative"],
    "Expansion.Conjunction"  :["also", "Expansion", "Conjunction"],
    "Expansion.Instantiation":["for", "Expansion", "Instantiation"],
    "Expansion.List"         :["and", "Expansion", "List"],
    "Expansion.Restatement"  :["specifically", "Expansion", "Restatement"],
    "Temporal.Asynchronous"  :["before", "Temporal", "Asynchronous"],
    "Temporal.Synchrony"     :["when", "Temporal", "Synchrony"],
    }
    
elif args.dataset == "conll16-test":      
    num_classes = 14 
    Processor = CoNLL15Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/CoNLL15-Imp"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'test')
    class_labels = Processor.get_labels()       
    label_words = {
    "Comparison.Concession"    :["nonetheless", "Comparison", "Concession"],
    "Comparison.Contrast"      :["but", "Comparison", "Contrast"], 
    "Contingency.Cause.Reason" :["because", "Contingency", "Reason"],
    "Contingency.Cause.Result" :["thus", "Contingency", "Result"],    
    "Contingency.Condition"    :["if", "Contingency", "Condition"],
    "Expansion.Alternative"    :["unless", "Expansion", "Alternative"],
    "Expansion.Alternative.Chosen alternative"  :["instead", "Expansion", "Chosen"],
    "Expansion.Conjunction"    :["also", "Expansion", "Conjunction"],
    "Expansion.Exception"      :["except", "Expansion", "Exception"],    
    "Expansion.Instantiation"  :["for", "Expansion", "Instantiation"],
    "Expansion.Restatement"    :["indeed", "Expansion", "Restatement"],
    "Temporal.Asynchronous.Precedence"  :["before", "Temporal", "Precedence"],
    "Temporal.Asynchronous.Succession"  :["previously", "Temporal", "Succession"],
    "Temporal.Synchrony"       :["as", "Temporal", "Synchrony"],
    }
    
elif args.dataset == "conll16-blind":      
    num_classes = 14 
    Processor = CoNLL15Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/CoNLL15-Imp-Blind"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'blind')
    class_labels = Processor.get_labels()    
    label_words = {
    "Comparison.Concession"    :["nonetheless", "Comparison", "Concession"],
    "Comparison.Contrast"      :["but", "Comparison", "Contrast"], 
    "Contingency.Cause.Reason" :["because", "Contingency", "Reason"],
    "Contingency.Cause.Result" :["thus", "Contingency", "Result"],    
    "Contingency.Condition"    :["if", "Contingency", "Condition"],
    "Expansion.Alternative"    :["unless", "Expansion", "Alternative"],
    "Expansion.Alternative.Chosen alternative"  :["instead", "Expansion", "Chosen"],
    "Expansion.Conjunction"    :["also", "Expansion", "Conjunction"],
    "Expansion.Exception"      :["except", "Expansion", "Exception"],    
    "Expansion.Instantiation"  :["for", "Expansion", "Instantiation"],
    "Expansion.Restatement"    :["indeed", "Expansion", "Restatement"],
    "Temporal.Asynchronous.Precedence"  :["before", "Temporal", "Precedence"],
    "Temporal.Asynchronous.Succession"  :["previously", "Temporal", "Succession"],
    "Temporal.Synchrony"       :["as", "Temporal", "Synchrony"],
    }

elif args.dataset == "pdtb3":      
    num_classes = 14 
    Processor = PDTB3Processor(num_labels=num_classes)
    
    data_dir = "./DiscoPrompt/PDTB3-Imp-Ji"
    dataset = {}
    dataset['train'] = Processor.get_examples(data_dir, 'train')
    dataset['validation'] = Processor.get_examples(data_dir, 'dev')
    dataset['test'] = Processor.get_examples(data_dir, 'test')
    class_labels = Processor.get_labels()  
    label_words = {
    "Comparison.Concession"  :["although", "Comparison", "Concession"],
    "Comparison.Contrast"    :["in contrast", "Comparison", "Contrast"],
    "Contingency.Cause+Belief" :["as", "Contingency", "Belief"],
    "Contingency.Cause"  :["because", "Contingency", "Cause"],
    "Contingency.Condition"  :["if", "Contingency", "Condition"],
    "Contingency.Purpose"    :["in order", "Contingency", "Purpose"],  
    "Expansion.Conjunction"  :["also", "Expansion", "Conjunction"],
    "Expansion.Equivalence"  :["in other words", "Expansion", "Equivalence"],        
    "Expansion.Instantiation":["for example", "Expansion", "Instantiation"],
    "Expansion.Level-of-detail":["specifically", "Expansion", "Level"],
    "Expansion.Manner"       :["thereby", "Expansion", "Manner"],
    "Expansion.Substitution"  :["instead", "Expansion", "Substitution"],
    "Temporal.Asynchronous"  :["then", "Temporal", "Asynchronous"],
    "Temporal.Synchronous"     :["meanwhile", "Temporal", "Synchronous"],
    }

else:
    raise NotImplementedError    

set_seed(args.seed)   
plm, tokenizer, model_config, WrapperClass = load_plm(args.model, args.model_name_or_path)

max_seq_l = args.max_seq_length
dataset_decoder_max_length = args.dataset_decoder_max_length
decoder_max_length = args.decoder_max_length
batchsize_t = args.batch_size
batchsize_e = args.batch_size_e
gradient_accumulation_steps = args.gradient_accumulation_steps
model_parallelize = True

template_id = args.template_id
mytemplate = PTRTemplate(model=plm, tokenizer=tokenizer).from_file(args.template_file, choice=template_id)
myverbalizer = DiscoVerbalizer(tokenizer, classes=class_labels, num_classes=num_classes, label_words = label_words)
print(mytemplate.text)

use_cuda = True
tune_plm = False
plm_eval_mode = True
prompt_model = PromptForClassification(plm=plm,template=mytemplate, verbalizer=myverbalizer, freeze_plm=(not tune_plm), plm_eval_mode=plm_eval_mode)

if use_cuda:
    prompt_model= prompt_model.cuda()

if model_parallelize:
    prompt_model.parallelize()

train_dataloader = PromptDataLoader(dataset=dataset["train"], template=mytemplate, tokenizer=tokenizer,
    tokenizer_wrapper_class=WrapperClass, max_seq_length=max_seq_l, decoder_max_length=decoder_max_length,
    batch_size=batchsize_t,shuffle=True, teacher_forcing=False, predict_eos_token=False,
    truncate_method="tail")

validation_dataloader = PromptDataLoader(dataset=dataset["validation"], template=mytemplate, tokenizer=tokenizer,
    tokenizer_wrapper_class=WrapperClass, max_seq_length=max_seq_l, decoder_max_length=decoder_max_length,
    batch_size=batchsize_e,shuffle=False, teacher_forcing=False, predict_eos_token=False,
    truncate_method="tail")

test_dataloader = PromptDataLoader(dataset=dataset["test"], template=mytemplate, tokenizer=tokenizer,
    tokenizer_wrapper_class=WrapperClass, max_seq_length=max_seq_l, decoder_max_length=decoder_max_length,
    batch_size=batchsize_e,shuffle=False, teacher_forcing=False, predict_eos_token=False,
    truncate_method="tail")
print("truncate rate: {}".format(train_dataloader.tokenizer_wrapper.truncate_rate), flush=True)
print("truncate rate: {}".format(validation_dataloader.tokenizer_wrapper.truncate_rate), flush=True)
print("truncate rate: {}".format(test_dataloader.tokenizer_wrapper.truncate_rate), flush=True)


generation_arguments = {
    "max_length": dataset_decoder_max_length,
}

max_steps = args.max_steps
loss_func = torch.nn.CrossEntropyLoss()
tot_step = max_steps

optimizer = "Adafactor"
prompt_lr = args.prompt_lr
print(prompt_lr)
warmup_step_prompt = args.warmup_step_prompt

if tune_plm: 
    no_decay = ['bias', 'LayerNorm.weight'] 
    optimizer_grouped_parameters1 = [
        {'params': [p for n, p in prompt_model.plm.named_parameters() if (not any(nd in n for nd in no_decay))], 'weight_decay': 0.01},
        {'params': [p for n, p in prompt_model.plm.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer1 = AdamW(optimizer_grouped_parameters1, lr=3e-5)
    scheduler1 = get_linear_schedule_with_warmup(
        optimizer1,
        num_warmup_steps=500, num_training_steps=tot_step)
else:
    optimizer1 = None
    scheduler1 = None


optimizer_grouped_parameters2 = [{'params': [p for name, p in prompt_model.template.named_parameters() if 'raw_embedding' not in name]}] 
if optimizer.lower() == "adafactor":
    optimizer2 = Adafactor(optimizer_grouped_parameters2,
                            lr=prompt_lr,
                            relative_step=False,
                            scale_parameter=False,
                            warmup_init=False)  
    scheduler2 = get_constant_schedule_with_warmup(optimizer2, num_warmup_steps=warmup_step_prompt) 
elif optimizer.lower() == "adamw":
    optimizer2 = AdamW(optimizer_grouped_parameters2, lr=prompt_lr) 
    scheduler2 = get_linear_schedule_with_warmup(
                    optimizer2,
                    num_warmup_steps=warmup_step_prompt, num_training_steps=tot_step) 


print(mytemplate.get_default_soft_token_ids())
print(optimizer_grouped_parameters2[0]['params'][0].size())
print("num of trainable parameters: %d" % ( sum(p.numel() for p in prompt_model.parameters() if p.requires_grad)))

eval_every_steps = args.eval_every_steps
project_root = args.project_root
this_run_unicode = args.ckpt_file
result_file = args.result_file

tot_loss = 0
log_loss = 0
final_best_val_acc = 0

best_val_acc = 0
best_val_f1score = 0 
best_val_acc_4class = 0
best_val_f1score_4class = 0

final_val_acc = 0
final_val_f1score = 0

final_best_glb_step = 0
best_val_acc_glb_step = 0
best_val_f1score_glb_step = 0
final_acc_f1score_glb_step = 0

glb_step = 0
actual_step = 0
leave_training = False











































        


            









































print("11class-Accuracy oriented Performance")
prompt_model.load_state_dict(torch.load(f"{args.eval_checkpoint}"))
prompt_model = prompt_model.cuda()

fianl_test_acc, final_test_F1_score, final_test_Acc_4class, final_test_F1_score_4class = evaluate(prompt_model, test_dataloader, dataset['test'], Processor, use_cuda, num_classes, test = True)
print("11Class - Testing Accuacry")
print(fianl_test_acc)
print("11Class - Testing F1 score")
print(final_test_F1_score)
print("4Class - Testing Accuacry")
print(final_test_Acc_4class)
print("4Class - Testing F1 score")
print(final_test_F1_score_4class)

with open(f"{result_file}", "w") as fout:
    fout.write(content_write)