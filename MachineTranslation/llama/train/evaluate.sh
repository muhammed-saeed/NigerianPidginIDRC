CUDA_VISIBLE_DEVICES=7 python evaluate.py \
    --load_8bit \
    --lora_weights "/PATH_TO/output/3_epochs_fixed_instruction_run/checkpoint-4600" \
    --base_model 'decapoda-research/llama-7b-hf' \
    --json_file "/PATH_TO/general-pidgin-modeling/llama/data/eval_dataset.json" \
    --pcm_preds_output_file "/PATH_TO/general-pidgin-modeling/llama/evaluationReal/test_pcm_preds.txt" \
    --en_preds_output_file "/PATH_TO/general-pidgin-modeling/llama/evaluationReal/test_english_preds.txt" \
    --results_output_file "/PATH_TO/general-pidgin-modeling/llama/evaluationReal/test_results.txt"