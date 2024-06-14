CUDA_VISIBLE_DEVICES=1 python3 evaluate.py \
--csv_file_path "/PATH/NigerianPidginIDRC/NaijaDiscoDataset/dataset/Mapped/mappedSenses/ImplicitEntrelRealPidginDiscoPromptToEval.csv" \
--model_name_or_path 'google/t5-v1_1-base/large'  \
--eval_checkpoint "PATH_TO_CHECKPOINT" \
--template_id 0 \
--max_steps 30000 \
--batch_size 4 \
--eval_every_steps 250  \
--dataset ji  \
--prompt_lr 0.3 >> Path to PRINT THE LOG of the output