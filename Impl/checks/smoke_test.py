from langchain_openai import ChatOpenAI

llm = ChatOpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama",
                 model="qwen14b-16k", temperature=0.2)
print(llm.invoke("Antworte mit dem Wort: bereit").content)
