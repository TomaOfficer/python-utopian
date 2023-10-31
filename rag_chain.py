def initialize_rag_chain():

    # Load documents
    from langchain.document_loaders.csv_loader import CSVLoader
    loader = CSVLoader(file_path='example_data/budget-breakdown.csv')

    # Split documents
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
    splits = text_splitter.split_documents(loader.load())

    # Embed and store splits
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OpenAIEmbeddings
    vectorstore = Chroma.from_documents(documents=splits,embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    # Prompt 
    # https://smith.langchain.com/hub/rlm/rag-prompt
    from langchain import hub
    rag_prompt = hub.pull("rlm/rag-prompt")

    # LLM
    from langchain.chat_models import ChatOpenAI
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # RAG chain 
    from langchain.schema.runnable import RunnablePassthrough
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | rag_prompt 
        | llm 
    )

    rag_chain.invoke("What is the biggest category of expense?")
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | rag_prompt 
        | llm 
    )
    
    return rag_chain

