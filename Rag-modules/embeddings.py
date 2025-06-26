from openai import OpenAI
import numpy as np
from config import OPENAI_KEY , EMBEDDING_MODEL
client = OpenAI(api_key=OPENAI_KEY)
def generate_embeddings(texts):
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[texts]  # Input should be a list of strings
        )
        embeddings = response.data[0].embedding
        return np.array(embeddings).astype('float32').reshape(1, -1)
    except Exception as e:
        print(f"Error : {e}")
        return None