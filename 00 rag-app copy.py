import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    load_dotenv()
    
    openai_endpoint = os.getenv("OPENAI_ENDPOINT")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat_model = os.getenv("CHAT_MODEL")
    embedding_model = os.getenv("EMBEDDING_MODEL")
    search_endpoint = os.getenv("SEARCH_ENDPOINT")
    search_api_key = os.getenv("SEARCH_API_KEY")
    index_name = os.getenv("INDEX_NAME")
    
    chat_client = AzureOpenAI(
        api_version = "2024-12-01-preview",
        azure_endpoint = openai_endpoint,
        api_key = openai_api_key
    )
    
    prompt = [
        {
            "role" : "system",
            "content" : "You are a travel assistant that provides information on travel service available from Margie's Travel."
        },
    ]
    
    while True:
        input_text = input("Enter your question (or type 'exit' to quit): ")
        if input_text.lower() == "exit":
            print("Exiting the application.")
            break
        elif input_text.strip() == "":
            print("Please enter a valid question.")
            continue
        
        prompt.append({"role" : "user", "content" : input_text})
        
        rag_params = {
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": index_name,
                        "authentication": {
                            "type": "api_key",
                            "api_key": search_api_key
                        },
                        "query_type": "vector",
                        "embedding_dependency": {
                            "type": "deployment_name",
                            "deployment_name": embedding_model
                        }
                    }
                }
            ]
        }

    respones = chat_client.chat.completions.create(
        model = chat_model,
        messages=prompt,
        extra_body=rag_params
    )
    
    completion = respones.choices[0].message.content
    print(completion)
    
    prompt.append({"role": "assistant", "content":completion})
        
if __name__ == "__main__":
    main()