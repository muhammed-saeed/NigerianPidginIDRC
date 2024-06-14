
CUDA_VISIBLE_DEVICES=4 python /PATH_TO/DiscoPrompt/DiscoPromptPidgin.py \
--template_id 0 --max_steps 30000 \
--csv_file_path "/PATH_TO/NPIDRC/BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEGiza.csv" \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-large \
--result_file /PATH_TO/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/Scratch/GizaPy/t5_v1_1_large/03LearningRateDiscoPromptClassification_PDTB2Scratch.txt \
--ckpt_file AlignOnly/scratch/GizaPy/large/DiscoPromptClassification_PDTB2_03LRAlignOnlyScratchGizaPy \
--prompt_lr 0.3 \
--epoch 1_000_000 \
--percentage 1 \
--project_root "/PATH_TO/DiscoPrompt" > "/PATH_TO/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/Scratch/GizaPy/t5_v1_1_large/t5V1_1_largeLog_0_3_learningRate_1M_epochs_GizaPyScratch.txt"

