import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_synthetic_testset():
    """
    Simulates how an automated QA generator converts raw context into structured 
    Question-Context-Ground_Truth evaluation tuples.
    """
    print("--- SYNTHETIC DATA GENERATOR INITIALIZED ---")
    
    # Raw knowledge context block
    sample_context = (
        "Parental Leave (HR-LEAVE-2026): Eligible parents receive up to 12 weeks of "
        "fully paid parental leave following the birth or adoption of a child."
    )
    
    print(f"Ingesting raw text: '{sample_context[:80]}...'")
    
    # In practice, students would call a generation LLM prompt:
    # "Given this context, generate a question that can be answered by it, and extract the exact ground truth."
    # Let's show the result of what would be generated:
    synthetic_case = {
        "query": "How many weeks of parental leave do employees get at Acme Corp?",
        "context": sample_context,
        "ground_truth": "Acme Corp provides up to 12 weeks of fully paid parental leave for new parents via birth or adoption.",
        "generated_output_v1": "Eligible employees get 12 weeks of fully paid parental leave."
    }
    
    print("\nGenerated Synthetic QA Pair:")
    print(json.dumps(synthetic_case, indent=2))
    
    # Save/Append to golden dataset
    dataset_file = "./data/golden_dataset.json"
    if os.path.exists(dataset_file):
        with open(dataset_file, "r") as f:
            data = json.load(f)
    else:
        data = []
        
    # Append if not already present
    if not any(tc["query"] == synthetic_case["query"] for tc in data):
        synthetic_case["id"] = f"tc_0{len(data)+1}"
        data.append(synthetic_case)
        with open(dataset_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nSuccessfully appended synthetic test case to '{dataset_file}'.")
    else:
        print("\nTest case already exists in dataset.")

if __name__ == "__main__":
    generate_synthetic_testset()
