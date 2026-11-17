import torch
from transformers import ( MambaConfig, MambaForCausalLM, AutoTokenizer, 
    Trainer, TrainingArguments, DataCollatorForLanguageModeling )
from datasets import Dataset
config = MambaConfig( vocab_size=50277,      # Match the tokenizer vocabulary size (e.g. GPT-2/EleutherAI tokenizers)
    d_model=256,           # Hidden size
    n_layer=4,             # Number of Mamba layers
    pad_token_id=50276,    # Pad token identifier
    bos_token_id=50256,     eos_token_id=50256 )
print("Initializing Mamba model from scratch...") # 2. Initialize the model with random weights
model = MambaForCausalLM(config) # 3. Load a tokenizer
tokenizer = AutoTokenizer.from_pretrained("state-spaces/mamba-130m-hf")
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token # 4. Create dummy training data (replace this with your text corpus)
dummy_texts = [ "The future of artificial intelligence in biological science is promising.",
    "Mamba is a state space model designed for efficient sequence modeling.",
    "Pretraining requires large corpora of text and many computational steps.",
    "We can train small models quickly on modern GPUs using huggingface trainer." ] * 25  # Replicate data to have a tiny training pool
def tokenize_function(examples): # Tokenize dataset
    return tokenizer(examples["text"], truncation=True, max_length=64)
raw_dataset = Dataset.from_dict({"text": dummy_texts})
tokenized_dataset = raw_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
training_args = TrainingArguments( output_dir="./mamba_pretrained",
    num_train_epochs=3, per_device_train_batch_size=4,
    logging_steps=10, learning_rate=5e-4,
    weight_decay=0.1, warmup_steps=5,
    fp16=torch.cuda.is_available(), # Use mixed precision if GPU is available
    remove_unused_columns=False )
trainer = Trainer( model=model, args=training_args, 
          train_dataset=tokenized_dataset, data_collator=data_collator, )
print("Starting training...")
trainer.train()
print("Training complete! Model saved to './mamba_pretrained'")
