import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from search import HybridRetriever
from google.antigravity import Agent, LocalAgentConfig

# Load Environment Variables
load_dotenv()

# Streamlit App Configurations
st.set_page_config(
    page_title="Agentic Enterprise RAG",
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

# ----------------- ADK CUSTOM TOOL DEFINITION -----------------
def search_company_policies(query: str) -> str:
    """Queries the internal database to find company remote work, travel, and security policies.

    Args:
        query: The search term or policy question, e.g., 'stipend' or 'hotel limit'.
    """
    if retriever is None:
        return "Error: Document index database is not loaded."
    
    # Run hybrid search
    results = retriever.hybrid_search(query, top_k=3)
    if not results:
        return "No policy documents matching that query were found."
        
    # Format matches into a structured block
    formatted_docs = []
    for idx, match in enumerate(results):
        formatted_docs.append(
            f"[Document {idx+1}]\n"
            f"Section: {match['metadata']['section']}\n"
            f"Doc Ref: {match['metadata']['doc_ref']}\n"
            f"Text: {match['text']}"
        )
    return "\n\n".join(formatted_docs)

# Title and Description
st.title("🔍 Agentic RAG Assistant (Powered by Antigravity SDK)")
st.markdown("""
Interact with the Acme Corp internal policies database via an autonomous AI Agent. 
The Agent determines when and how to search the knowledge base using custom query tools.
""")

# Sidebar settings
st.sidebar.title("Agent Status & Telemetry")
api_key_set = bool(os.getenv("GEMINI_API_KEY"))

if api_key_set:
    st.sidebar.success("✅ Gemini API Key detected.")
else:
    st.sidebar.warning("⚠️ No Gemini API Key found. Run in simulated tool-execution mode.")

st.sidebar.info("""
**Agent Stack:**
- **Framework:** Antigravity SDK (ADK)
- **Model:** `gemini-3.5-flash` (Default)
- **Tools:** `search_company_policies`
""")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Async runner for Agent Chat
async def run_agent_chat(user_input: str):
    # Configure the Antigravity Agent
    config = LocalAgentConfig(
        system_instructions=(
            "You are an Acme Corp internal policies assistant. "
            "Use the search_company_policies tool to lookup answers to the user's question. "
            "Cite the documents you retrieve (e.g. [Document 1] or Document Reference code) in your final response. "
            "If the tool returns no matching documents, inform the user that you cannot find the answer in the policies."
        ),
        tools=[search_company_policies]
    )
    
    # Initialize the agent
    async with Agent(config=config) as agent:
        # Send query to the agent
        response = await agent.chat(user_input)
        return await response.text()

# User Input
if prompt := st.chat_input("Ask a question about internal policies..."):
    # Display user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Process retrieval
    with st.chat_message("assistant"):
        with st.spinner("Agent formulating search query..."):
            if api_key_set:
                try:
                    # Run the async agent chat
                    llm_response = asyncio.run(run_agent_chat(prompt))
                except Exception as e:
                    st.error(f"Error during Agent execution: {e}")
                    api_key_set = False # Fall back
            
            if not api_key_set:
                # Simulated local tool execution fallback
                st.info("[Simulating ADK Tool Execution]")
                context = search_company_policies(prompt)
                llm_response = (
                    "### [Offline Sim Response]\n"
                    f"The agent executed `search_company_policies('{prompt}')` and found:\n\n"
                    f"{context}\n\n"
                    "*Configure a `GEMINI_API_KEY` to allow the agent to autonomously parse and synthesize responses.*"
                )
                
        # Display response
        st.markdown(llm_response)
        st.session_state.messages.append({"role": "assistant", "content": llm_response})
