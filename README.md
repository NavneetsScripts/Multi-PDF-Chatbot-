# PDF Chatbot Application

A comprehensive Streamlit-based chatbot web application that allows users to upload and query multiple PDF documents using Large Language Models (LLMs) from OpenAI and Hugging Face. The application features semantic search, conversational memory, and secure API key management.

## ðŸš€ Features

- **Multi-PDF Support**: Upload and process multiple PDF documents simultaneously
- **Dual LLM Integration**: Support for both OpenAI and Hugging Face models
- **Semantic Search**: Advanced vector-based document search using embeddings
- **Conversational Memory**: Maintains context across multiple conversation turns
- **Secure API Management**: Safe handling of API keys and sensitive data
- **Modern UI/UX**: Clean, responsive interface built with Streamlit
- **Performance Monitoring**: Built-in performance tracking and optimization
- **Error Handling**: Comprehensive error handling and logging
- **Local Vector Database**: Uses ChromaDB for efficient document storage and retrieval

## ðŸ“‹ Prerequisites

- Python 3.8 or higher
- OpenAI API key (for OpenAI models)
- Hugging Face API key (for Hugging Face models)
- At least 4GB RAM (8GB recommended for Hugging Face models)

## ðŸ› ï¸ Installation

1. **Clone or download the project**
   `ash
   git clone <repository-url>
   cd pdf-chatbot-app
   `

2. **Create a virtual environment**
   `ash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   `

3. **Install dependencies**
   `ash
   pip install -r requirements.txt
   `

4. **Set up environment variables**
   `ash
   # Copy the example environment file
   cp config/.env.example .env
   
   # Edit .env file with your API keys
   # OPENAI_API_KEY=your_openai_api_key_here
   # HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   `

## ðŸš€ Quick Start

1. **Start the application**
   `ash
   streamlit run app.py
   `

2. **Open your browser**
   - Navigate to http://localhost:8501
   - The application will open in your default browser

3. **Configure the chatbot**
   - Select your preferred AI providers in the sidebar
   - Click "Initialize Chatbot" to start

4. **Upload PDF documents**
   - Use the file uploader in the sidebar
   - Click "Process Files" to add documents to the knowledge base

5. **Start chatting**
   - Type your questions in the chat interface
   - The bot will search through your documents and provide answers

## ðŸ“– Usage Guide

### Uploading Documents

1. Click "Browse files" in the sidebar
2. Select one or more PDF files
3. Click "Process Files" to extract text and create embeddings
4. Wait for processing to complete

### Asking Questions

1. Type your question in the chat input field
2. Click "Send" or press Enter
3. The bot will search through your documents and provide an answer
4. View sources by expanding the "Sources" section

### Managing Conversations

- **New Conversation**: Start a fresh conversation session
- **Save Conversation**: Save current conversation to disk
- **Clear Database**: Remove all uploaded documents

## âš™ï¸ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | OpenAI API key | Required |
| OPENAI_MODEL | OpenAI model to use | gpt-3.5-turbo |
| OPENAI_EMBEDDING_MODEL | OpenAI embedding model | 	ext-embedding-ada-002 |
| HUGGINGFACE_API_KEY | Hugging Face API key | Optional |
| HUGGINGFACE_MODEL | Hugging Face model | microsoft/DialoGPT-medium |
| HUGGINGFACE_EMBEDDING_MODEL | HF embedding model | sentence-transformers/all-MiniLM-L6-v2 |
| MAX_FILE_SIZE_MB | Maximum file size | 50 |
| MAX_CHUNK_SIZE | Text chunk size | 1000 |
| CHUNK_OVERLAP | Chunk overlap | 200 |
| MAX_CONVERSATION_HISTORY | Max conversation history | 10 |

### Performance Settings

- **Enable Caching**: Reduces API calls for repeated queries
- **Chunk Size**: Larger chunks provide more context but use more memory
- **Chunk Overlap**: Higher overlap improves context continuity

## ðŸ—ï¸ Architecture

`
pdf-chatbot-app/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ chatbot.py          # Main chatbot orchestrator
â”‚   â”œâ”€â”€ pdf_processor.py    # PDF text extraction and chunking
â”‚   â”œâ”€â”€ vector_database.py  # ChromaDB integration
â”‚   â”œâ”€â”€ embedding_service.py # Embedding generation
â”‚   â”œâ”€â”€ llm_service.py      # LLM integration
â”‚   â”œâ”€â”€ conversation_memory.py # Conversation management
â”‚   â””â”€â”€ security.py         # Security and error handling
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ config.py           # Configuration management
â”‚   â””â”€â”€ .env.example       # Environment variables template
â”œâ”€â”€ data/                   # Vector database storage
â”œâ”€â”€ docs/                   # Documentation
â”œâ”€â”€ tests/                  # Unit tests
â”œâ”€â”€ app.py                  # Main Streamlit application
â””â”€â”€ requirements.txt        # Python dependencies
`

## ðŸ”§ Advanced Configuration

### Custom Models

You can use different models by modifying the configuration:

`python
# For OpenAI
OPENAI_MODEL = "gpt-4"  # Use GPT-4 instead of GPT-3.5
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"  # Use newer embedding model

# For Hugging Face
HUGGINGFACE_MODEL = "microsoft/DialoGPT-large"  # Use larger model
HUGGINGFACE_EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"  # Better embeddings
`

### Performance Optimization

1. **For faster processing**: Use smaller chunk sizes
2. **For better accuracy**: Use larger chunk sizes with more overlap
3. **For memory efficiency**: Use OpenAI API instead of local Hugging Face models
4. **For offline use**: Use Hugging Face models (requires more RAM)

## ðŸš€ Deployment

### Local Deployment

The application runs locally by default. For production use:

1. **Set production environment variables**
2. **Configure logging levels**
3. **Set up proper file permissions**
4. **Use a reverse proxy (nginx) for HTTPS**

### Cloud Deployment

#### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Add environment variables in the Streamlit Cloud dashboard
4. Deploy!

#### Docker Deployment

`dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
`

#### AWS/Azure/GCP

1. Use container services (ECS, Container Instances, Cloud Run)
2. Set up proper IAM roles for API access
3. Configure environment variables
4. Set up monitoring and logging

## ðŸ§ª Testing

Run the test suite:

`ash
python -m pytest tests/
`

## ðŸ“Š Monitoring and Logging

- **Logs**: Stored in logs/ directory
- **Performance metrics**: Available in the UI
- **Error tracking**: Comprehensive error logging and user feedback

## ðŸ”’ Security Considerations

- API keys are stored securely in environment variables
- File uploads are validated for size and type
- Input sanitization prevents injection attacks
- Conversation data is stored locally (not sent to external services)

## ðŸ¤ Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## ðŸ“„ License

This project is licensed under the MIT License - see the LICENSE file for details.

## ðŸ†˜ Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your API keys are correctly set in the .env file
   - Check that the keys have the correct format

2. **Memory Issues**
   - Reduce chunk size in configuration
   - Use OpenAI API instead of local Hugging Face models
   - Close other applications to free up RAM

3. **Slow Performance**
   - Enable caching in configuration
   - Use smaller embedding models
   - Reduce the number of documents processed simultaneously

4. **File Upload Issues**
   - Check file size limits
   - Ensure PDF files are not corrupted
   - Verify file permissions

### Getting Help

- Check the logs in the logs/ directory
- Review the error messages in the UI
- Ensure all dependencies are correctly installed
- Verify your API keys are valid and have sufficient credits

## ðŸ”® Future Enhancements

- [ ] Support for additional document formats (DOCX, TXT, etc.)
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Document summarization
- [ ] Export conversation history
- [ ] User authentication and multi-user support
- [ ] Advanced analytics and insights
- [ ] Integration with cloud storage services
