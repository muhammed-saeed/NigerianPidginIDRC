
CUDA_VISIBLE_DEVICES=0 python /local/musaeed/DiscoPrompt/DiscoPromptPidgin.py \
--template_id 0 --max_steps 30000 \
--csv_file_path "/local/musaeed/NPIDRC/FullTransferMethod/Implicit/ScriptsTransfer/DisContinous/simAlignRoBERTa/data/ModifiedMain.csv" \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-base \
--result_file "/local/musaeed/NPIDRC/FullTransferMethod/Results/FullTransfer/Scratch/SimAlignRoBERTa/t5_v1_1_base/03LearningRateDiscoPromptClassification_PDTB2Scratch.txt" \
--ckpt_file FullTransferCheckpoints/SimAlignRoBERTa/Scratch/base/DiscoPromptClassification_PDTB2_03LRScratchSimAlignRoBERTa \
--prompt_lr 0.3 \
--epoch 1_000_000 \
--percentage 1 \
--project_root "/local/musaeed/DiscoPrompt" > "/local/musaeed/NPIDRC/FullTransferMethod/Results/FullTransfer/Scratch/SimAlignRoBERTa/t5_v1_1_base/t5V1_1_baseLog_0_3_learningRate_1M_epochs_SimAlignRoBERTaScratch.txt"

