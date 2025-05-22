import streamlit as st
import os
import tempfile
import uuid
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from datetime import datetime
import pandas as pd

# Constitution of Kazakhstan text (embedded directly)
CONSTITUTION_TEXT = """
CONSTITUTION OF THE REPUBLIC OF KAZAKHSTAN

We, the people of Kazakhstan, united by a common historic fate, creating a state on the indigenous Kazakh land, considering ourselves a peace-loving and civil society, dedicated to the ideals of freedom, equality and concord, wishing to take a worthy place in the world community, realizing our high responsibility before the present and future generations, proceeding from our sovereign right, adopt this Constitution.

SECTION I. GENERAL PROVISIONS

Article 1
1. The Republic of Kazakhstan proclaims itself a democratic, secular, legal and social state whose highest values are an individual, his life, rights and freedoms.
2. The fundamental principles of the activity of the Republic are: public concord and political stability; economic development for the benefit of the entire people; Kazakhstani patriotism; and resolution of the most important issues of state life by democratic methods including voting at republican referenda or in the Parliament.

Article 2
1. The Republic of Kazakhstan is a unitary state with a presidential form of government.
2. The sovereignty of the Republic extends to its entire territory. The state ensures the integrity, inviolability and inalienability of its territory.

Article 3
1. The people shall be the only source of state power.
2. The people shall exercise power directly through republican and local referenda and free elections, as well as delegate the exercise of their power to state institutions.
3. No one shall have the right to usurp state power.

Article 4
1. The acting law of the Republic of Kazakhstan shall be: norms of the Constitution, laws corresponding to the Constitution, other normative legal acts, international treaty and other obligations of the Republic, as well as normative resolutions of the Constitutional Council and the Supreme Court of the Republic.
2. The Constitution shall have the highest juridical force and direct application on the entire territory of the Republic.
3. International treaties ratified by the Republic shall have priority over its laws. The procedure and conditions of application of international treaties and other obligations of the Republic of Kazakhstan shall be determined by legislation of the Republic.

Article 5
1. The Republic of Kazakhstan shall recognize ideological and political diversity.
2. The formation of public associations pursuing the goals or actions directed toward a violent change of the constitutional system, violation of the integrity of the Republic, undermining the security of the state, inciting social, racial, national, religious, class and tribal strife, as well as the formation of unauthorized paramilitary units, shall be prohibited.

Article 6
1. In the Republic of Kazakhstan, the Kazakh language shall be the state language.
2. In state institutions and local self-administrative bodies the Russian language shall be officially used on equal grounds along with the Kazakh language.
3. The state shall promote conditions for the study and development of the languages of the people of Kazakhstan.

Article 7
1. The state symbols of the Republic of Kazakhstan shall be the flag, emblem and anthem. Their description and the order of official use shall be established by constitutional laws.
2. The capital of Kazakhstan shall be the city of Nur-Sultan. The status of the capital shall be determined by law.

Article 8
The Republic of Kazakhstan shall respect the principles and norms of international law, pursue a policy of cooperation and good neighborly relations between states, their equality and non-interference in internal affairs, peaceful settlement of international disputes and renunciation of the first use of military force.

Article 9
The Republic of Kazakhstan shall have citizenship. Citizenship of the Republic of Kazakhstan shall be acquired and terminated according to the law. A citizen of the Republic may not be deprived of citizenship, the right to change citizenship, or be exiled outside of Kazakhstan. A citizen of Kazakhstan may not be extradited to a foreign state unless otherwise provided by international treaties of the Republic.

SECTION II. THE INDIVIDUAL AND CITIZEN

Article 10
1. Citizenship of the Republic of Kazakhstan shall be acquired and terminated on the grounds and in accordance with the procedure established by law.
2. Citizenship of the Republic of Kazakhstan shall be single and equal regardless of the grounds of its acquisition.
3. A citizen of the Republic may not be deprived of citizenship or the right to change it.

Article 11
A citizen of the Republic of Kazakhstan may not be extradited to a foreign state unless otherwise provided for by international treaties of the Republic.

Article 12
1. Human rights and freedoms in the Republic of Kazakhstan shall be recognized and guaranteed in accordance with this Constitution.
2. Human rights and freedoms shall belong to everyone from birth, be recognized as absolute and inalienable, and determine the contents and application of laws and other normative legal acts.
3. A citizen of the Republic of Kazakhstan may not be deprived of citizenship or the right to change it, or be exiled from Kazakhstan.

Article 13
1. Everyone shall have the right to recognition of his legal personality and may not be subjected to any discrimination for reasons of origin, social, property status, occupation, sex, race, nationality, language, attitude toward religion, convictions, place of residence or any other circumstances.
2. No one may be subjected to torture, violence or other cruel or degrading treatment or punishment.

Article 14
1. Everyone shall be equal before the law and court of law.
2. No one may be subjected to any discrimination for reasons of origin, social, property status, occupation, sex, race, nationality, language, attitude toward religion, convictions, place of residence or any other circumstances.

Article 15
1. Everyone shall have the right to life.
2. No one shall have the right to arbitrarily deprive another of life. Capital punishment is prohibited.

Article 16
1. Everyone shall have the right to personal freedom.
2. No one may be subjected to arrest and detention except on legal grounds. A person may be detained without a court decision for a period not exceeding seventy-two hours. Preventive detention for a longer period may be applied only by court decision.

Article 17
1. The dignity of the individual shall be inviolable.
2. No one may be subjected to torture, violence, or other cruel or degrading treatment or punishment.
3. Medical, scientific or other experiments may not be conducted on a person without his voluntary consent.

Article 18
1. Everyone shall have the right to inviolability of private life, personal and family secrets, protection of honor and dignity.
2. Everyone shall have the right to confidentiality of personal deposits and savings, correspondence, telephone conversations, postal, telegraph and other messages. Limitations of this right shall be allowed only in cases and according to the procedure established by law.

Article 19
1. Marriage and family, motherhood, fatherhood and childhood shall be under the protection of the state.
2. Care of children and their upbringing are the natural right and duty of parents.
3. Children may not be subjected to any discrimination and shall have equal rights regardless of their origin and social status.
4. Working children, disabled children and children deprived of parental care shall be entitled to special protection by the state.

Article 20
1. Freedom of speech and creative work shall be guaranteed. Censorship shall be prohibited.
2. Everyone shall have the right to freely receive and disseminate information by any means not prohibited by law. The list of information constituting state secrets of the Republic of Kazakhstan shall be determined by law.

Article 21
1. Everyone shall have the right to preserve his ethnic identity.
2. Everyone shall have the right to use his native language and culture, to freely choose the language of communication, upbringing, education and creative work.

Article 22
1. Everyone shall have the right to freedom of conscience.
2. The exercise of the right to freedom of conscience must not condition or restrict general civil, political, economic rights and freedoms.

Article 23
1. Citizens of the Republic shall have the right to freedom of association. The activities of public associations shall be regulated by law.
2. No one may be compelled to belong or not belong to any association.

Article 24
1. Everyone shall have the right to freedom of movement and choice of residence within the territory of the Republic, as well as the right to leave the Republic.
2. This right may be restricted only by laws and only when it is necessary to protect national security, public order, health and morality of the population.

SECTION III. THE PRESIDENT

Article 40
1. The President of the Republic of Kazakhstan shall be the head of state, its highest official determining the main directions of the domestic and foreign policy of the state and representing Kazakhstan within the country and in international relations.
2. The President shall be the symbol and guarantor of the unity of the people and the state power, inviolability of the Constitution, rights and freedoms of an individual and citizen.
3. The President shall ensure coordinated functioning and interaction of all branches of state power and accountability of the institutions of power to the people.

Article 41
1. The President shall be elected by universal, equal and direct suffrage under a secret ballot for a term of seven years.
2. A citizen of the Republic by birth, not younger than forty years of age, with a perfect command of the state language and having lived in Kazakhstan for not less than fifteen years, may be elected President of the Republic.
3. The same person may not be elected President of the Republic more than two times in a row.

This is a sample portion of the Constitution. The full document contains many more articles covering government structure, rights, and legal procedures.
"""

# Initialize ChromaDB
@st.cache_resource
def init_chromadb():
    client = chromadb.PersistentClient(path="./chroma_db")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    try:
        collection = client.get_collection(name="constitution_collection", embedding_function=sentence_transformer_ef)
    except:
        collection = client.create_collection(name="constitution_collection", embedding_function=sentence_transformer_ef)

    return collection

# Initialize LLM
def init_llm():
    api_key = st.session_state.get("groq_api_key", "")
    if not api_key:
        return None

    return ChatGroq(
        api_key=api_key,
        model_name="llama3-70b-8192",
    )

# Function to process document texts
def process_documents(texts, metadata_list):
    collection = init_chromadb()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    all_chunks = []
    all_metadatas = []

    for i, text in enumerate(texts):
        if text and len(text.strip()) > 50:  # Only process non-empty texts
            chunks = text_splitter.split_text(text)
            metadatas = [metadata_list[i]] * len(chunks)

            all_chunks.extend(chunks)
            all_metadatas.extend(metadatas)

    if all_chunks:
        # Generate IDs for each chunk
        ids = [str(uuid.uuid4()) for _ in range(len(all_chunks))]

        # Add documents to ChromaDB
        collection.add(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=ids
        )

    return len(all_chunks)

# Function to extract text from different file types
def extract_text_from_file(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.getbuffer())
        file_path = tmp.name

    try:
        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            text = "\n".join([page.page_content for page in pages])
        elif file_extension == '.docx':
            loader = Docx2txtLoader(file_path)
            pages = loader.load()
            text = "\n".join([page.page_content for page in pages])
        elif file_extension in ['.txt', '.md']:
            loader = TextLoader(file_path)
            pages = loader.load()
            text = "\n".join([page.page_content for page in pages])
        else:
            text = f"Unsupported file format: {file_extension}"

        return text
    except Exception as e:
        return f"Error processing file: {str(e)}"
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.unlink(file_path)

# Function to search for relevant context
def search_context(query, k=5):
    collection = init_chromadb()
    try:
        results = collection.query(
            query_texts=[query],
            n_results=k
        )

        if results['documents'] and len(results['documents'][0]) > 0:
            context = "\n\n".join(results['documents'][0])
            # Debug: show what context was found
            st.write(f"**Debug - Found {len(results['documents'][0])} relevant chunks**")
            st.text(f"First chunk preview: {context[:200]}...")
            return context, results['metadatas'][0]
        else:
            st.error("No relevant context found in database")
            return "", []
    except Exception as e:
        st.error(f"Error searching context: {str(e)}")
        return "", []

# Function to generate response
def generate_response(query, context, metadatas):
    llm = init_llm()
    if not llm:
        return "Please enter your Groq API key in the sidebar first."

    if not context:
        return "I don't have enough information in my knowledge base to answer your question. Please make sure the Constitution data has been loaded or upload relevant documents."

    # Format metadata into a string for better context
    sources = [meta.get('source', 'Unknown') for meta in metadatas]
    unique_sources = list(set(sources))
    metadata_str = "Sources: " + ", ".join(unique_sources)

    system_prompt = f"""You are an AI assistant specialized in the Constitution of the Republic of Kazakhstan.
    Answer the user's question directly using the provided context information from the Constitution.

    Context from the Constitution of Kazakhstan:
    {context}

    Instructions:
    - Answer directly and confidently based on the provided context
    - Do NOT apologize or say the context doesn't contain information - it does
    - Be specific and cite relevant articles when possible
    - Provide clear, comprehensive answers
    - Do not start with phrases like "I apologize" or "The context doesn't contain"
    - Start directly with the answer to the question
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Based on the Constitution of Kazakhstan context provided, please answer: {query}")
    ]

    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to log the conversation
def log_conversation(query, response, source_docs):
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Format source documents
    sources = [doc.get('source', 'Unknown') for doc in source_docs]
    unique_sources = list(set(sources))

    st.session_state.conversation_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response,
        "sources": ", ".join(unique_sources)
    })

# Function to check if constitution is loaded
def is_constitution_loaded():
    collection = init_chromadb()
    try:
        result = collection.count()
        return result > 0
    except:
        return False

# Main Streamlit app
def main():
    st.set_page_config(page_title="Kazakhstan Constitution AI Assistant", layout="wide")

    # Initialize session state for conversation history
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Set up sidebar for API key and document loading
    with st.sidebar:
        st.title("Configuration")

        # API Key input
        groq_api_key = st.text_input("Enter your Groq API Key:", type="password",
                                     help="Get your API key from https://console.groq.com")
        if groq_api_key:
            st.session_state.groq_api_key = groq_api_key

        st.divider()

        # Constitution loading status
        constitution_loaded = is_constitution_loaded()
        if constitution_loaded:
            st.success("✅ Constitution data is loaded!")
        else:
            st.warning("⚠️ Constitution data not loaded yet")

        # Load built-in constitution
        if st.button("Load Built-in Constitution", disabled=constitution_loaded):
            with st.spinner("Loading Constitution data..."):
                # Clear existing data first
                try:
                    collection = init_chromadb()
                    all_ids = collection.get()['ids']
                    if all_ids:
                        collection.delete(ids=all_ids)
                except:
                    pass

                chunks_added = process_documents(
                    [CONSTITUTION_TEXT],
                    [{"source": "Constitution of Kazakhstan (Built-in)", "date_added": datetime.now().strftime("%Y-%m-%d")}]
                )

                if chunks_added > 0:
                    st.success(f"Successfully loaded the Constitution! Added {chunks_added} chunks to the database.")
                    st.rerun()
                else:
                    st.error("Failed to load Constitution data.")

        st.divider()

        # File uploader for additional documents
        st.subheader("Upload Additional Documents")
        uploaded_files = st.file_uploader("Upload files (PDF, TXT, DOCX, MD)",
                                          accept_multiple_files=True,
                                          type=["pdf", "txt", "docx", "md"])

        if uploaded_files and st.button("Process Uploaded Files"):
            with st.spinner("Processing uploaded files..."):
                all_texts = []
                all_metadatas = []

                for file in uploaded_files:
                    text = extract_text_from_file(file)
                    if not text.startswith("Error") and not text.startswith("Unsupported"):
                        all_texts.append(text)
                        all_metadatas.append({
                            "source": file.name,
                            "date_added": datetime.now().strftime("%Y-%m-%d")
                        })
                    else:
                        st.error(f"Failed to process {file.name}: {text}")

                if all_texts:
                    chunks_added = process_documents(all_texts, all_metadatas)
                    st.success(f"Successfully processed {len(all_texts)} files! Added {chunks_added} chunks to the database.")

        st.divider()

        # Database management
        st.subheader("Database Management")
        if st.button("Clear All Data", type="secondary"):
            try:
                collection = init_chromadb()
                # Delete all documents
                all_ids = collection.get()['ids']
                if all_ids:
                    collection.delete(ids=all_ids)
                    st.success("All data cleared!")
                    st.rerun()
                else:
                    st.info("No data to clear.")
            except Exception as e:
                st.error(f"Error clearing data: {str(e)}")

        # View conversation history
        if st.button("Export Conversation History"):
            if st.session_state.conversation_history:
                df = pd.DataFrame(st.session_state.conversation_history)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f"conversation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No conversation history to export.")

    # Main content area
    st.title("🇰🇿 Kazakhstan Constitution AI Assistant")
    st.markdown("Ask questions about the Constitution of the Republic of Kazakhstan")

    # Check prerequisites
    if not st.session_state.get("groq_api_key"):
        st.error("⚠️ Please enter your Groq API key in the sidebar to continue.")
        st.stop()

    if not is_constitution_loaded():
        st.error("⚠️ Please load the Constitution data first using the 'Load Built-in Constitution' button in the sidebar.")
        st.stop()

    # Chat interface
    st.subheader("Ask a Question")

    # Example questions
    with st.expander("💡 Example Questions"):
        example_questions = [
            "What are the main principles of the Republic of Kazakhstan?",
            "What are the requirements to become President of Kazakhstan?",
            "What rights and freedoms are guaranteed to citizens?",
            "What is the official language of Kazakhstan?",
            "How long is the presidential term?",
            "What are the symbols of the state?"
        ]

        for question in example_questions:
            if st.button(question, key=question):
                st.session_state.current_query = question

    # Query input
    query = st.text_input("Your question:", value=st.session_state.get("current_query", ""))

    if st.button("Submit", type="primary") and query:
        with st.spinner("Searching for relevant information and generating response..."):
            context, metadatas = search_context(query)

            if context:
                response = generate_response(query, context, metadatas)
                log_conversation(query, response, metadatas)

                # Display response
                st.subheader("📋 Response:")
                st.write(response)

                # Display sources
                if metadatas:
                    st.subheader("📚 Sources:")
                    unique_sources = list(set([meta.get('source', 'Unknown') for meta in metadatas]))
                    for source in unique_sources:
                        st.write(f"• {source}")

                # Clear the current query
                if "current_query" in st.session_state:
                    del st.session_state.current_query
            else:
                st.error("No relevant information found. Please ensure the Constitution data is properly loaded.")

    # Display conversation history
    if st.session_state.conversation_history:
        st.divider()
        st.subheader("💬 Conversation History")

        for i, entry in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5 conversations
            with st.expander(f"Q: {entry['query'][:100]}{'...' if len(entry['query']) > 100 else ''}", expanded=(i==0)):
                st.write(f"**🕒 Time:** {entry['timestamp']}")
                st.write(f"**❓ Question:** {entry['query']}")
                st.write(f"**💡 Answer:** {entry['response']}")
                st.write(f"**📖 Sources:** {entry['sources']}")

if __name__ == "__main__":
    main()