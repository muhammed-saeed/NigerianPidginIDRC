CUDA_VISIBLE_DEVICES=1 python evaluatte.py \
    --load_8bit \
    --base_model 'decapoda-research/llama-7b-hf' \
    --lora_weights '/PATH_TO/general-pidgin-modeling/llama/output/sanityCheck_3epoch' \
