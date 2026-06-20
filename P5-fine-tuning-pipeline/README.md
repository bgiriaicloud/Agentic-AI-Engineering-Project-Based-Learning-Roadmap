# Project 5: Fine-Tuning Pipeline
*Duration: 4 Weeks | Focus: Model Optimization*

## 📖 Project Brief
Students will build a parameter-efficient fine-tuning (PEFT/LoRA) pipeline to adapt a small open-source LLM (such as `TinyLlama/TinyLlama-1.1B-Chat-v1.0` or `google/gemma-2b-it`) to generate structured JSON formats that strictly conform to **Google Antigravity SDK (ADK) Response Schemas** and Pydantic validation rules.

---

## 🎯 Learning Objectives
- Master **LoRA (Low-Rank Adaptation)** and **QLoRA (Quantized LoRA)** concepts.
- Format raw text datasets into instruction-response JSON pairs mapping to Pydantic structures.
- Understand tokenization padding, truncation, and packing strategies.
- Implement training configurations using HuggingFace `SFTTrainer` and `BitsAndBytesConfig` (for 4-bit/8-bit quantization).
- Mitigate Out-of-Memory (OOM) errors using Gradient Accumulation, Gradient Checkpointing, and mixed precision (FP16/BF16).
- Evaluate fine-tuned models on structured response accuracy to ensure zero schema compliance failures.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                      QLORA FINE-TUNING PIPELINE                        |
+------------------------------------------------------------------------+
|                                                                        |
|  [Raw Data Instructions] (sample_instructions.json)                    |
|             │                                                          |
|             ▼ (Apply Pydantic prompt format structures)                |
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
|     [Output schema check passes google-antigravity structured checks]   |
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
11. **Verify structured syntax formatting:** Code simulated before-and-after prints inside `src/inference.py` to show how untuned models output loose text while the tuned model outputs strict JSON matching the schema.
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

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Dataset Engineering** | 20% | Instruction formatting, token verification, and train/test splits. |
| **Quantization & LoRA Config** | 25% | Correct target modules and rank parameters (r, alpha, dropout) setup. |
| **Trainer Setup & Runs** | 30% | Correct hyperparameters (learning rate, weight decay, epoch counts). |
| **Inference Comparison** | 15% | Structured output comparison showing schema-compliant results. |
| **Code Integrity & Documentation** | 10% | Clean, well-structured, and documented files. |
