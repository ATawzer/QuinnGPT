# QuinnGPT
Query Unreal Instantly with Nearest Neighbors - Library dedicated to serving the latest documentation on unreal, its source code, your source code and plugins with GPT powered embeddings and chat, served with ChromaDB.

# Introduction
With the power of GPT, unreal engine development has definitely acclerated greatly for many developers. The only downside is the training window stopped right before UE5. QuinnGPT, named after one of the two iconic mannequins that ship with UE5, solves this by providing an interface for scraping the latest docs into a chromadb vectorstore and then allowing chat-like interactions with the latest documentation. In Addition, the vector store can populate your own source code, custom plugins or other sources of documentation as needed.

# Getting Started
## Environment
To use QuinnGPT you will need a MongoDB backend for tracking scraping and other operations. After installing MongoDB on your machine the rest will be handled by QuinnDB after giving it your credentials. Additionally, for vector storage ChromaDB will be used with OpenAI serving as the sole embeddings provider (for now). Your .env file should look like 
'''
OPENAI_KEY=... # Get this from OpenAI
MONGODB_HOST=localhost:27017 # Or hosted server
MONGODB_USERNAME=... # Username you configure on your database
MONGODB_PASSWORD=... # Password you configure on your database
MONGODB_AUTH_SOURCE=... # Which database in your mongo client to authenticate against
'''

When in the directory run 
'''
pipenv install
''' 
Which will download the necessary libraries, including invoke which will be used for orchestrating.

## Getting Data
For the process to work you will need to add unreal documentation into your vector database. The DocsScraper class is designed for this very purpose and be called via python. To trigger the process run the following command when in the pipenv shell:
'''
inv run-all
'''
This will begin the processing of collecting all the pages and caching them locally to .cache/. In total the Unreal Documentation will be ~10,000 pages and 400MB. In the future the process will support the direct writing of docs to the chromaDB, for now and for stability the Vector Database is populated with the cached files.






This is a work in progress, more to come. . . 
