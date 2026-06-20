import os
import sys

def run_dry_run_inference():
    """
    Simulates base vs fine-tuned output predictions.
    """
    print("\n=======================================================")
    print("      INFERENCE COMPARISON - DRY RUN SIMULATION        ")
    print("=======================================================")
    print("Simulating weight merging using PEFT PeftModel:")
    print("  `model = PeftModel.from_pretrained(base_model, adapter_dir)`")
    
    test_queries = [
        "What is the policy code for remote work workspace setups?",
        "Explain password requirements at Acme Corp."
    ]
    
    # Pre-calculated comparisons illustrating the effect of instruction fine-tuning
    comparisons = {
        "What is the policy code for remote work workspace setups?": {
            "base": (
                "I am not sure about the exact policy code. Acme Corp has several codes for remote works "
                "such as HR-001 or REMOTE-RULES. You might want to check the files or search the portal."
            ),
            "fine_tuned": (
                "The policy code for remote workspace setups is HR-REMOTE-2026."
            )
        },
        "Explain password requirements at Acme Corp.": {
            "base": (
                "Passwords should generally be strong, secure, and contain special symbols. Make sure to "
                "change your passwords often to keep your accounts secure."
            ),
            "fine_tuned": (
                "Passwords must be at least 12 characters, contain letters, numbers, and symbols, and rotate every 90 days."
            )
        }
    }
    
    for query in test_queries:
        print(f"\nQUERY: {query}")
        print("-" * 50)
        print(f"🔴 BASE UNTUNED LLM RESPONSE:\n{comparisons[query]['base']}")
        print(f"🟢 FINE-TUNED MODEL RESPONSE:\n{comparisons[query]['fine_tuned']}")
        print("-" * 50)

def run_actual_inference():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    
    base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    adapter_dir = "./lora_adapters"
    
    print(f"Loading Base Model: {base_model_name}")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    print(f"Loading LoRA adapters from: {adapter_dir}")
    # Wrap model with PeftModel
    model = PeftModel.from_pretrained(model, adapter_dir)
    
    # Run test prompt
    prompt = "### Instruction:\nWhat is the policy code for remote work workspace setups?\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    print("Generating outputs...")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=64)
        
    print("\n--- RESPONSE FROM MERGED MODEL ---")
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

def main():
    has_gpu = False
    try:
        import torch
        has_gpu = torch.cuda.is_available()
    except ImportError:
        pass
        
    adapter_exists = os.path.exists("./lora_adapters/adapter_config.json")
    
    if has_gpu and adapter_exists:
        try:
            run_actual_inference()
        except Exception as e:
            print(f"Error loading GPU libraries: {e}. Defaulting to simulated comparison.")
            run_dry_run_inference()
    else:
        run_dry_run_inference()

if __name__ == "__main__":
    main()
