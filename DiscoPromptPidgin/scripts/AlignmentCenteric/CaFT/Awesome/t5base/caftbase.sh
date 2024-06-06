
CUDA_VISIBLE_DEVICES=3 python /local/musaeed/DiscoPrompt/DiscoPromptPidginContinueFromCheckpoint.py \
--template_id 0 --max_steps 30000 \
--csv_file_path "/local/musaeed/NPIDRC/BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEAwesomeAlign.csv" \
--batch_size 4 --eval_every_steps 250 \
--shouldResumeTrainingFromCheckpoint True \
--resume_from_checkpoint "/local/musaeed/DiscoPrompt/ckpts/englishBaseT5_v_1_base/DiscoPromptClassification_PDTB2.ckpt" \
--dataset ji --model_name_or_path google/t5-v1_1-base \
--result_file /local/musaeed/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/CaFT/Awesome/t5_v1_1_base/03LearningRateDiscoPromptClassification_PDTB2CaFT.txt \
--ckpt_file AlignOnly/Awesome/CaFT/base/DiscoPromptClassification_PDTB2_03LRAlignOnlyCaFTAwesome \
--prompt_lr 0.3 \
--epoch 1_000_000 \
--percentage 1 \
--project_root "/local/musaeed/DiscoPrompt" > "/local/musaeed/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/CaFT/Awesome/t5_v1_1_base/t5V1_1_baseLog_0_3_learningRate_1M_epochs_AwesomeCaFT.txt"

