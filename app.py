import streamlit as st
import logging
import os
from typing import List, Dict, Any
import time
from datetime import datetime

# Import our custom modules
from src.chatbot import PDFChatbot
from config.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="ðŸ“š",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .success-message {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
    .sidebar-section {
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = "Ready"
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = None

def initialize_chatbot():
    """Initialize the chatbot with selected providers"""
    try:
        # Get provider selections from sidebar
        embedding_provider = st.session_state.get('embedding_provider', 'openai')
        llm_provider = st.session_state.get('llm_provider', 'openai')
        
        # Initialize chatbot
        st.session_state.chatbot = PDFChatbot(
            embedding_provider=embedding_provider,
            llm_provider=llm_provider
        )
        
        # Start new conversation
        st.session_state.conversation_id = st.session_state.chatbot.start_new_conversation()
        
        st.success("Chatbot initialized successfully!")
        return True
        
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {str(e)}")
        return False

def display_chat_message(role: str, content: str, metadata: Dict[str, Any] = None):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Assistant:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
        
        # Show metadata if available
        if metadata and not metadata.get('error'):
            if metadata.get('similar_documents'):
                with st.expander("ðŸ“„ Sources"):
                    for doc in metadata['similar_documents'][:3]:  # Show top 3
                        st.write(f"**{doc['metadata'].get('filename', 'Unknown')}** (Similarity: {doc['similarity']:.2f})")
                        st.write(doc['document'][:200] + "...")

def process_uploaded_files(uploaded_files: List[Any]) -> bool:
    """Process uploaded PDF files"""
    if not uploaded_files:
        return False
    
    try:
        st.session_state.processing_status = "Processing files..."
        
        # Process files
        results = st.session_state.chatbot.process_uploaded_pdfs(uploaded_files)
        
        # Display results
        if results["success"]:
            st.session_state.processing_status = f"Processed {len(results['success'])} files successfully"
            
            # Show success details
            for success in results["success"]:
                st.success(f"âœ… {success['filename']}: {success['chunks']} chunks from {success['pages']} pages")
            
            # Show errors if any
            if results["errors"]:
                for error in results["errors"]:
                    st.warning(f"âš ï¸ {error}")
            
            return True
        else:
            st.session_state.processing_status = "Processing failed"
            for error in results["errors"]:
                st.error(f"âŒ {error}")
            return False
            
    except Exception as e:
        st.session_state.processing_status = "Processing failed"
        st.error(f"Error processing files: {str(e)}")
        return False

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">ðŸ“š PDF Chatbot</h1>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>{Config.APP_DESCRIPTION}</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## âš™ï¸ Configuration")
        
        # Provider selection
        st.markdown("### ðŸ¤– AI Providers")
        embedding_provider = st.selectbox(
            "Embedding Provider",
            ["openai", "huggingface"],
            index=0,
            key="embedding_provider"
        )
        
        llm_provider = st.selectbox(
            "LLM Provider",
            ["openai", "huggingface"],
            index=0,
            key="llm_provider"
        )
        
        # Initialize chatbot button
        if st.button("ðŸš€ Initialize Chatbot", type="primary"):
            initialize_chatbot()
        
        # File upload section
        st.markdown("### ðŸ“ Document Upload")
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files to query"
        )
        
        if uploaded_files and st.session_state.chatbot:
            if st.button("ðŸ“¤ Process Files"):
                process_uploaded_files(uploaded_files)
        
        # Database stats
        if st.session_state.chatbot:
            st.markdown("### ðŸ“Š Database Stats")
            stats = st.session_state.chatbot.get_database_stats()
            if stats:
                st.metric("Total Documents", stats.get("total_documents", 0))
            
            if st.button("ðŸ—‘ï¸ Clear Database"):
                if st.session_state.chatbot.clear_database():
                    st.success("Database cleared!")
                else:
                    st.error("Failed to clear database")
        
        # Conversation management
        if st.session_state.chatbot:
            st.markdown("### ðŸ’¬ Conversation")
            if st.button("ðŸ†• New Conversation"):
                st.session_state.conversation_id = st.session_state.chatbot.start_new_conversation()
                st.session_state.messages = []
                st.success("Started new conversation!")
            
            if st.button("ðŸ’¾ Save Conversation"):
                st.session_state.chatbot.save_conversation()
                st.success("Conversation saved!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        st.markdown("## ðŸ’¬ Chat Interface")
        
        # Display chat messages
        for message in st.session_state.messages:
            display_chat_message(
                message["role"],
                message["content"],
                message.get("metadata")
            )
        
        # Chat input
        if st.session_state.chatbot:
            user_input = st.text_input(
                "Ask a question about your documents:",
                placeholder="Type your question here...",
                key="user_input"
            )
            
            if st.button("Send", type="primary") and user_input:
                # Add user message to display
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Generate response
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.generate_response(user_input)
                
                # Add assistant response to display
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["response"],
                    "metadata": {
                        "similar_documents": response.get("similar_documents", []),
                        "error": response.get("error", False)
                    },
                    "timestamp": datetime.now().isoformat()
                })
                
                # Rerun to show new messages
                st.rerun()
        else:
            st.info("Please initialize the chatbot using the sidebar configuration.")
    
    with col2:
        # Status and information
        st.markdown("## ðŸ“ˆ Status")
        st.info(f"**Status:** {st.session_state.processing_status}")
        
        if st.session_state.conversation_id:
            st.info(f"**Conversation ID:** {st.session_state.conversation_id}")
        
        # Recent messages
        if st.session_state.chatbot:
            st.markdown("## ðŸ“ Recent Messages")
            recent_messages = st.session_state.chatbot.get_recent_messages(3)
            for msg in recent_messages:
                st.text(f"{msg['role']}: {msg['content'][:50]}...")

if __name__ == "__main__":
    main()
