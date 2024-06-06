
CUDA_VISIBLE_DEVICES=6 python /local/musaeed/DiscoPrompt/DiscoPrompt.py \
--template_id 0 --max_steps 30000 \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-small \
--result_file /local/musaeed/DiscoPrompt/results/t5smallEglish50percenttraining/DiscoPromptClassification_PDTB2.txt \
--ckpt_file t5smallEnglish50percenttraining/DiscoPromptClassification_PDTB2 \
--prompt_lr 0.3 \
--percentage 0.5 \
--project_root "/local/musaeed/DiscoPrompt"