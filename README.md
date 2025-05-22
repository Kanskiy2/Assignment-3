# Kazakhstan Constitution AI Assistant - Installation and Usage Guide

## Overview

This application is an AI-powered assistant specifically designed to answer questions about the Constitution of the Republic of Kazakhstan. It features:

- A chat interface for asking questions about the constitution
- Integration with Groq's LLM API for generating responses
- ChromaDB as a vector database for storing and retrieving relevant information
- Document upload functionality for adding custom files
- Conversation history tracking and export capabilities

## Requirements

- Python 3.8+
- Groq API key (sign up at [groq.com](https://console.groq.com))

## Installation

1. Clone or download the application code from the repository.

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install streamlit requests beautifulsoup4 chromadb langchain langchain-groq pandas python-docx2txt uuid
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Instructions

### Initial Setup

1. When you first run the application, you'll see a sidebar on the left for configuration and a main area for chat interaction.

2. Enter your Groq API key in the sidebar (you can sign up for one at [groq.com](https://console.groq.com)).

3. Load the Constitution data by clicking "Load Constitution from Website" in the sidebar. This will scrape the content from the official website and add it to the vector database.

### Asking Questions

1. Type your question about the Kazakhstan Constitution in the text input field.

2. Click "Submit" to get a response. The AI will:
   - Search the vector database for relevant information
   - Generate a response using the Groq LLM
   - Display the response along with the sources used

### Uploading Custom Documents

1. In the sidebar, use the file uploader to select one or more files (supported formats: PDF, TXT, DOCX, MD).

2. Click "Process Uploaded Files" to extract text and add it to the vector database.

3. Once processed, you can ask questions that include information from these documents.

### Viewing and Exporting Conversation History

1. Your questions and the AI's responses are automatically saved in the conversation history.

2. To export the history as a CSV file, click "Export Conversation History" in the sidebar.

## Features

### Vector Database Storage

- All documents are chunked and stored in ChromaDB with semantic embeddings
- Documents maintain metadata about their source and date added
- Similar documents are retrieved based on semantic search when questions are asked

### Document Processing

- Supports multiple file formats (PDF, DOCX, TXT, MD)
- Automatically chunks large documents for better retrieval
- Maintains source information for citations

### Conversation Management

- Records timestamps, questions, answers, and sources used
- Allows export to CSV for record-keeping

## Troubleshooting

- If you see "Please enter your Groq API key" message, ensure you've added your API key in the sidebar
- If the application cannot find information for your question, try:
  - Rephrasing your question
  - Loading the Constitution data again
  - Uploading additional relevant documents

- If you encounter errors with file processing, check that your files are in supported formats

## Extending the Application

This MVP can be extended in several ways:

- Add support for more LLM providers (OpenAI, Gemini, etc.)
- Implement user authentication for personalized experiences
- Add support for more document formats
- Implement document summarization features
- Add multi-language support
