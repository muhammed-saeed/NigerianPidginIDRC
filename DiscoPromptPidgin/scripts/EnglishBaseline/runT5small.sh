
CUDA_VISIBLE_DEVICES=6 python /local/musaeed/DiscoPrompt/DiscoPrompt.py \
--template_id 0 --max_steps 30000 \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path t5-small \
--result_file /local/musaeed/DiscoPrompt/results/englishBaselineT5V1_1_Small/DiscoPromptClassification_PDTB2.txt \
--ckpt_file englishBaselineT5V1_1Small \
--prompt_lr 0.3
--project_root "/local/musaeed/NPIDRC/DiscoPrompt"