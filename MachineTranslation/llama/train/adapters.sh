CUDA_VISIBLE_DEVICES=1,2,3,4 python /PATH_TO/alpaca-lora/adapters.py \
    --base_model 'decapoda-research/llama-7b-hf' \
    --data_path '/PATH_TO/general-pidgin-modeling/llamma/data/sample_bidirectional_translation.json' \
    --output_dir '/PATH_TO/general-pidgin-modeling/llamma/output_model_adapters'\
    --wandb_project 'lamma adapters first test'