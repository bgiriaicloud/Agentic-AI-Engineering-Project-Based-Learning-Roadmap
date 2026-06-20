import os
import json
import pandas as pd
import streamlit as st
from evaluator import RAGEvaluator

st.set_page_config(
    page_title="RAG Evaluation Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RAG Quality & Evaluation Dashboard")
st.markdown("""
Evaluate, log, and benchmark Large Language Model outputs for **Faithfulness** (hallucination checks) and **Answer Relevancy**.
""")

# Load Golden Dataset
DATASET_PATH = "./data/golden_dataset.json"
RESULTS_PATH = "./data/evaluation_results.json"

@st.cache_data
def load_dataset():
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r") as f:
            return json.load(f)
    return []

test_cases = load_dataset()

# Sidebar actions
st.sidebar.header("Controls")
if st.sidebar.button("🚀 Run Evaluation Suite"):
    with st.spinner("Evaluating test suite cases..."):
        evaluator = RAGEvaluator()
        evaluator.run_suite(DATASET_PATH)
        st.sidebar.success("Suite ran successfully! Refreshing data...")
        st.cache_data.clear()

# Load Results
def load_results():
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH, "r") as f:
            return json.load(f)
    return []

eval_results = load_results()

if not eval_results:
    st.info("💡 Run the evaluation suite using the sidebar button to generate metrics charts.")
else:
    # Convert to pandas DF
    df = pd.DataFrame(eval_results)
    
    # Calculate Averages
    avg_faith_v1 = df["v1_faithfulness"].mean()
    avg_rel_v1 = df["v1_relevance"].mean()
    avg_faith_v2 = df["v2_faithfulness"].mean()
    avg_rel_v2 = df["v2_relevance"].mean()
    
    # Metrics display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="V1 Avg Faithfulness", value=f"{avg_faith_v1:.2f}")
    with col2:
        st.metric(label="V1 Avg Relevancy", value=f"{avg_rel_v1:.2f}")
    with col3:
        st.metric(label="V2 Avg Faithfulness (Hallucinated)", value=f"{avg_faith_v2:.2f}", delta=f"{avg_faith_v2 - avg_faith_v1:.2f}", delta_color="inverse")
    with col4:
        st.metric(label="V2 Avg Relevancy (Hallucinated)", value=f"{avg_rel_v2:.2f}", delta=f"{avg_rel_v2 - avg_rel_v1:.2f}", delta_color="inverse")

    st.markdown("### 📋 Test Case Comparison Matrix")
    st.dataframe(df.style.highlight_min(axis=0, color="rgba(255, 0, 0, 0.2)", subset=["v2_faithfulness", "v2_relevance"]))

    # Compare Charts
    st.markdown("### 📈 Visualizing Faithfulness Drift")
    chart_data = pd.DataFrame({
        "Test Case": df["id"],
        "V1 Faithfulness (Grounded)": df["v1_faithfulness"],
        "V2 Faithfulness (Hallucinated)": df["v2_faithfulness"]
    }).set_index("Test Case")
    st.bar_chart(chart_data)

# Test cases deep dive
st.markdown("### 🔍 Test Case Details")
for tc in test_cases:
    with st.expander(f"Case {tc['id']}: {tc['query']}"):
        st.markdown(f"**Context Document:**\n> *{tc['context']}*")
        st.markdown(f"**Ground Truth (Expected):**\n`{tc['ground_truth']}`")
        
        c1, c2 = st.columns(2)
        with c1:
            st.success("✅ **Model Output V1 (Grounded)**")
            st.write(tc["generated_output_v1"])
        with c2:
            st.error("❌ **Model Output V2 (Hallucinated)**")
            st.write(tc["generated_output_v2_hallucinated"])
