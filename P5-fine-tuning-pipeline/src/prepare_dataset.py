import os
import json
from datasets import Dataset

DATA_PATH = "./data"
INPUT_FILE = os.path.join(DATA_PATH, "sample_instructions.json")
OUTPUT_FILE = os.path.join(DATA_PATH, "processed_dataset.json")

def format_prompt(sample):
    """
    Formats the instruction data into a single text block suitable for instruction tuning.
    """
    instruction = sample.get("instruction", "")
    user_input = sample.get("input", "")
    output = sample.get("output", "")
    
    if user_input:
        text = f"### Instruction:\n{instruction}\n\n### Input:\n{user_input}\n\n### Response:\n{output}"
    else:
        text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
        
    return {"text": text}

def main():
    print("--- STEP 1: Loading Instruction Dataset ---")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please create it first.")
        return
        
    with open(INPUT_FILE, "r") as f:
        raw_data = json.load(f)
        
    print(f"Loaded {len(raw_data)} raw instruction pairs.")
    
    print("\n--- STEP 2: Applying Prompt Template ---")
    processed_records = [format_prompt(item) for item in raw_data]
    
    print("Sample Formatted Prompt:")
    print("-" * 50)
    print(processed_records[0]["text"])
    print("-" * 50)
    
    # Save the processed dataset
    with open(OUTPUT_FILE, "w") as f:
        json.dump(processed_records, f, indent=2)
        
    print(f"\nSaved processed dataset to '{OUTPUT_FILE}'.")
    
    # Showcase integration with HuggingFace datasets library
    hf_dataset = Dataset.from_list(processed_records)
    print(f"HuggingFace Dataset loaded: {hf_dataset}")

if __name__ == "__main__":
    main()
