
CUDA_VISIBLE_DEVICES=6 python /local/musaeed/DiscoPrompt/DiscoPrompt.py \
--template_id 0 --max_steps 30000 \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-large \
--result_file /local/musaeed/DiscoPrompt/results/englishBaselineT5_v_1_1large/DiscoPromptClassification_PDTB2.txt \
--ckpt_file englishBaseT5_v_1_large/DiscoPromptClassification_PDTB2 \
--prompt_lr 0.3 \
--project_root "/local/musaeed/DiscoPrompt" > "/local/musaeed/DiscoPrompt/results/englishBaselineT5_v_1_1large/t5V1_1LargeLog.txt"