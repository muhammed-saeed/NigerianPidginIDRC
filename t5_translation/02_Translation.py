import os
import logging
import pandas as pd
from simpletransformers.t5 import T5Model, T5Args
import argparse
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)
def train_t5_model(train_data_path, checkpoint_path, wandb_project, best_model, n_gpu):
    train_df = pd.read_csv(train_data_path, sep="\t").astype(str)
    model_args = T5Args()
    model_args.max_seq_length = 128
    model_args.train_batch_size = 16
    model_args.eval_batch_size = 16
    model_args.num_train_epochs = 20
    model_args.evaluate_during_training = False
    model_args.evaluate_during_training_steps = 30000
    model_args.use_multiprocessing = False
    model_args.fp16 = True
    model_args.save_model_every_epoch = False
    model_args.save_steps = -1
    model_args.save_eval_checkpoints = True
    model_args.no_cache = True
    model_args.reprocess_input_data = True
    model_args.overwrite_output_dir = True
    model_args.preprocess_inputs = False
    model_args.n_gpu = n_gpu
    model_args.num_return_sequences = 1
    model_args.output_dir = checkpoint_path
    model_args.wandb_project = wandb_project
    model_args.use_early_stopping = True
    model = T5Model("t5", "t5-base", args=model_args)
    model.train_model(train_df)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a T5 Model.")
    parser.add_argument("--train_data_path", default="/PATH_TO/NPIDRC/dev/data/promptEngineeringNoDevNorTestupdated_file.tsv",
                        help="Path to the training data file in TSV format.")
    parser.add_argument("--checkpoint_path", default="/PATH_TO/NPIDRC/t5_translation/newPhrasecheckpoint16Batch",
                        help="Path to the checkpoint directory.")
    parser.add_argument("--wandb_project", default="Tony 1, 16 batch prefix translate English to Nigerian Pidgin",
                        help="Name of project in Weights & Biases.")
    parser.add_argument("--best_model", help="Path to the best_model")
    parser.add_argument("--n_gpu", type=int, default=3, help="Number of GPUS")
    args = parser.parse_args()
    train_t5_model(args.train_data_path, args.checkpoint_path,
                   args.wandb_project, args.best_model, args.n_gpu)
