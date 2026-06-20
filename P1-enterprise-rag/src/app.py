import os
import streamlit as st
from dotenv import load_dotenv
from search import HybridRetriever

# Load Environment Variables
load_dotenv()

# Streamlit App Configurations
st.set_page_config(
    page_title="Enterprise Knowledge Base RAG",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Retriever state
@st.cache_resource
def get_retriever():
    try:
        return HybridRetriever()
    except Exception as e:
        st.error(f"Failed to load vector database indices: {e}")
        st.info("💡 Did you run `python src/ingest.py` first?")
        return None

retriever = get_retriever()

# Title and Description
st.title("🔍 Acme Corp Enterprise RAG Assistant")
st.markdown("""
Welcome to the internal policy assistant. Ask questions regarding HR, Remote work, Travel, and Device Security policies.
""")

# Sidebar settings
st.sidebar.title("Configuration & Metadata")
api_key_set = bool(os.getenv("GEMINI_API_KEY"))

if api_key_set:
    st.sidebar.success("✅ Gemini API Key detected.")
else:
    st.sidebar.warning("⚠️ No Gemini API Key found. Running in local Offline Simulation mode.")

top_k = st.sidebar.slider("Number of retrieved chunks", min_value=1, max_value=5, value=3)

# Chat logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about internal company policies..."):
    # Display user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Process retrieval
    if retriever is None:
        with st.chat_message("assistant"):
            st.error("RAG pipeline is not initialized. Please ensure the indices are built.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                retrieved_chunks = retriever.hybrid_search(prompt, top_k=top_k)
                
            if not retrieved_chunks:
                st.write("No matching documents found in the database.")
            else:
                # Show retrieved chunks in an expander for transparency (great for educational purposes)
                with st.expander("📂 Retrieved Reference Chunks"):
                    for idx, chunk in enumerate(retrieved_chunks):
                        st.markdown(f"**Chunk {idx+1} (RRF Score: {chunk['rrf_score']:.4f})**")
                        st.markdown(f"*Source:* `{chunk['metadata']['source']}` | *Section:* `{chunk['metadata']['section']}` | *Ref:* `{chunk['metadata']['doc_ref']}`")
                        st.text(chunk['text'])
                        st.markdown("---")
                
                # Context Formatting
                context_str = ""
                for idx, chunk in enumerate(retrieved_chunks):
                    context_str += f"[Doc {idx+1}] Ref: {chunk['metadata']['doc_ref']} (Section: {chunk['metadata']['section']})\nContent: {chunk['text']}\n\n"
                
                # Model query/synthesis
                with st.spinner("Formulating answer..."):
                    llm_response = ""
                    
                    if api_key_set:
                        try:
                            import google.generativeai as genai
                            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                            
                            system_instruction = (
                                "You are an internal HR assistant answering questions using only the provided context snippets. "
                                "Use bracketed citations referencing the documents (e.g., [Doc 1]) to support your assertions. "
                                "If you cannot find the answer in the provided documents, state clearly that the information is not "
                                "found in the internal policies. Do not hallucinate."
                            )
                            
                            model = genai.GenerativeModel(
                                model_name="gemini-1.5-flash",
                                system_instruction=system_instruction
                            )
                            
                            llm_prompt = f"User Question: {prompt}\n\nContext Documents:\n{context_str}"
                            response = model.generate_content(llm_prompt)
                            llm_response = response.text
                            
                        except Exception as e:
                            st.error(f"Error calling Gemini API: {e}")
                            st.info("Falling back to local heuristic response.")
                            api_key_set = False # trigger fallback
                            
                    # Local fallback / simulated LLM response
                    if not api_key_set:
                        # Construct a basic response summarizing context
                        llm_response = "### [Offline Simulated Response]\n"
                        llm_response += "Based on internal documentation matches, here is the relevant text found:\n\n"
                        for idx, chunk in enumerate(retrieved_chunks):
                            llm_response += f"- **{chunk['metadata']['section']}** (Reference `{chunk['metadata']['doc_ref']}`):\n  > \"{chunk['text'][:250]}...\" [Doc {idx+1}]\n\n"
                        llm_response += "\n*Note: Add a `GEMINI_API_KEY` to your environment to enable actual LLM conversational text generation.*"
                
                # Output Response
                st.markdown(llm_response)
                st.session_state.messages.append({"role": "assistant", "content": llm_response})
