
CUDA_VISIBLE_DEVICES=6 python /PATH_TO/DiscoPrompt/DiscoPrompt.py \
--template_id 0 --max_steps 30000 \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-base \
--result_file /PATH_TO/DiscoPrompt/results/englishBaselineT5_v_1_1base/DiscoPromptClassification_PDTB2.txt \
--ckpt_file englishBaseT5_v_1_base/DiscoPromptClassification_PDTB2 \
--prompt_lr 0.3 \
--project_root "/PATH_TO/DiscoPrompt" >  "/PATH_TO/DiscoPrompt/results/englishBaselineT5_v_1_1base/t5_v1_1base.log"