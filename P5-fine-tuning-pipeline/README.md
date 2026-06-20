# Project 5: Fine-Tuning Pipeline
*Duration: 4 Weeks | Focus: Model Optimization*

## 📖 Project Brief
Students will build a parameter-efficient fine-tuning (PEFT/LoRA) pipeline to adapt a small open-source LLM (such as `TinyLlama/TinyLlama-1.1B-Chat-v1.0` or `google/gemma-2b-it`) to a specialized domain (e.g. customer service or domain-specific legal definitions) using HuggingFace Transformers, PEFT, and PyTorch.

---

## 🎯 Learning Objectives
- Master **LoRA (Low-Rank Adaptation)** and **QLoRA (Quantized LoRA)** concepts.
- Format raw text datasets into instruction-response JSON pairs.
- Understand tokenization padding, truncation, and packing strategies.
- Implement training configurations using HuggingFace `SFTTrainer` and `BitsAndBytesConfig` (for 4-bit/8-bit quantization).
- Mitigate Out-of-Memory (OOM) errors using Gradient Accumulation, Gradient Checkpointing, and mixed precision (FP16/BF16).
- Evaluate fine-tuned weights using perplexity and human evaluation.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                      QLORA FINE-TUNING PIPELINE                        |
+------------------------------------------------------------------------+
|                                                                        |
|  [Raw Data Instructions] (sample_instructions.json)                    |
|             │                                                          |
|             ▼ (Apply prompt format structure)                          |
|  [Processed Prompt Text]                                               |
|             │                                                          |
|             ▼ (Load Tokenizer mapping)                                 |
|  [Tokenized Input Sequences]                                           |
|             │                                                          |
|             ├────────────────────────┐                                 |
|             ▼                        ▼ (Freeze core parameters)        |
|  [Base LLM Weights] (NF4)     [LoRA Adapter Parameters] (FP16)         |
|  (e.g., TinyLlama 1.1B)       (q_proj, v_proj target modules)          |
|             │                        │                                 |
|             └───────────┬────────────┘                                 |
|                         │                                              |
|                         ▼ (SFTTrainer execution checks)                |
|              /// Supervised Training Loop \\\                          |
|              \\\                              ///                      |
|                         │                                              |
|                         ▼ (Save checkpoints)                           |
|                 [Saved Adapter Weights] (lora_adapters/)               |
|                         │                                              |
|                         ▼ (Merge weights during model load)            |
|               [Evaluation & Inference Comparison]                      |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to build and execute the Fine-Tuning Pipeline:

1. **Environment Setup:** Set up your python virtual environment and verify CUDA/GPU availability. Install torch and transformers libraries.
2. **Collect Raw Dataset:** Examine raw instruction sets at `data/sample_instructions.json` showing instruction, input, and output keys.
3. **Format Prompt Templates:** Implement `format_prompt` inside `src/prepare_dataset.py` to structure prompts with standard instruction headers (e.g. `### Instruction:\n`).
4. **Export Clean Dataset:** Run `python src/prepare_dataset.py` to tokenize inputs and output `data/processed_dataset.json`.
5. **Configure Quantization Parameters:** Inside `src/train.py`, setup `BitsAndBytesConfig` defining 4-bit Nf4 quantization type and FP16 compute datatypes.
6. **Configure LoRA Hyperparameters:** Setup `LoraConfig` inside `src/train.py` defining rank (`r=8`), scaling alpha (`lora_alpha=16`), and target modules.
7. **Load Base Model & Tokenizer:** Incorporate model load logic inside `src/train.py` that downloads the base tokenizer and model weights with quantization configurations applied.
8. **Configure Training Arguments:** Define hyperparameters inside `src/train.py` including gradient accumulation and learning rate values.
9. **Implement CPU Mock Training:** Build `run_dry_run_training` inside `src/train.py` to simulate epochs and save sample configurations without CUDA dependency.
10. **Build Comparative Inference Scorer:** Inside `src/inference.py`, set up PeftModel wrappers to load base model weights and load the saved adapters.
11. **Implement Inference Mock Comparison:** Code simulated before-and-after prints inside `src/inference.py` to display comparative changes.
12. **Run Training & Verification:** Execute the trainer (`python src/train.py`) and inference comparison script (`python src/inference.py`) to test adapter weight overlays.

---

## 📅 Week-by-Week Deliverables

### Week 1: Dataset Preparation & Preprocessing
- Collect raw text datasets, write cleaning scripts.
- Format data into standardized instruction-response structure.
- **Deliverable:** `src/prepare_dataset.py` and formatted JSON dataset.

### Week 2: Quantization & LoRA Training Configuration
- Load a base model in 4-bit precision.
- Define `LoraConfig` target modules (e.g., `q_proj`, `v_proj`).
- Write standard HuggingFace training scripts.
- **Deliverable:** Executable SFT trainer script `src/train.py`.

### Week 3: Model Training & Tuning
- Run training loops (on local GPU or free Colab GPU notebook).
- Track loss metrics and save checkpoint files.
- **Deliverable:** Set of saved adapter weights.

### Week 4: Inference Comparison & Evaluation
- Load base model and load saved adapter weights to merge them.
- Compare predictions from the un-tuned base model against the fine-tuned model.
- **Deliverable:** Comparative test script `src/inference.py`.

---

## 📁 Repository Structure
```
P5-fine-tuning-pipeline/
├── README.md
├── requirements.txt
├── data/
│   └── sample_instructions.json
└── src/
    ├── prepare_dataset.py
    ├── train.py
    └── inference.py
```

---

## 🚀 Setup & Execution

### 1. Install Dependencies
Ensure you use a virtual environment:
```bash
pip install -r requirements.txt
```

### 2. Format Raw Data
```bash
python src/prepare_dataset.py
```

### 3. Run Training (Dry-run or actual GPU training)
```bash
python src/train.py
```

### 4. Evaluate and Run Inference
Compare base vs fine-tuned responses:
```bash
python src/inference.py
```

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Dataset Engineering** | 20% | Instruction formatting, token verification, and train/test splits. |
| **Quantization & LoRA Config** | 25% | Correct target modules and rank parameters (r, alpha, dropout) setup. |
| **Trainer Setup & Runs** | 30% | Correct hyperparameters (learning rate, weight decay, epoch counts). |
| **Inference Comparison** | 15% | Structured output comparison between base and adapter weights. |
| **Code Integrity & Documentation** | 10% | Clean, well-structured, and documented files. |

---

## 🛠️ Troubleshooting & Tips
- **CUDA Out of Memory:** If training fails due to VRAM limits, set `per_device_train_batch_size=1` and set `gradient_accumulation_steps=4` inside `src/train.py`. Enabling `gradient_checkpointing=True` also helps.
- **CPU training:** If a GPU is not present, the scripts contain fallback checks to run dry-run steps on a CPU.
