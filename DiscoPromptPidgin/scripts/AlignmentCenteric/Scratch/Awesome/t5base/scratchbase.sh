
CUDA_VISIBLE_DEVICES=7 python /PATH_TO/DiscoPrompt/DiscoPromptPidgin.py \
--template_id 0 --max_steps 30000 \
--csv_file_path "/PATH_TO/NPIDRC/BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEAwesomeAlign.csv" \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-base \
--result_file /PATH_TO/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/Scratch/Awesome/t5_v1_1_base/03LearningRateDiscoPromptClassification_PDTB2Scratch.txt \
--ckpt_file AlignOnly/scratch/AwesomeAlign/base/DiscoPromptClassification_PDTB2_03LRAlignOnlyScratchAwesome24May \
--prompt_lr 0.3 \
--epoch 1_000_000 \
--percentage 1 \
--project_root "/PATH_TO/DiscoPrompt" > "/PATH_TO/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/Scratch/Awesome/t5_v1_1_base/t5V1_1_baseLog_0_3_learningRate_1M_epochs_AwesomeScratch.txt"

