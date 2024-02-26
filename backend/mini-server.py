from langchain.agents import tool
from dotenv import load_dotenv
# from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_community.llms.llamacpp import LlamaCpp
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, tool
from langchain.globals import set_debug
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import ast
from diseases.parkinson import Parkinson
from diseases.diabetes import Diabetes


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allows CORS for your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

set_debug(True)


llm = LlamaCpp(
    model_path=r"C:\Users\thiru\Documents\apps\ai_models\Gen_AI\Text_Gen\llama-2-7b-chat.Q8_0.gguf",
    temperature=0.75,
    max_tokens=50,
    top_p=1,
    verbose=True,
)

llm.bind(stop=["User:", "Human:", "\n", "/n", "?\n", "Assistant:"])


def parkinson(query: str) -> str:
    """Takes in a dictionary of key value pairs {
    'MDVP:Fo(Hz)': 119.99200,
    'MDVP:Fhi(Hz)': 157.30200,
    'MDVP:Flo(Hz)': 74.99700,
    'MDVP:Jitter(%)': 0.00784,
    .....
    'spread2': 0.266482,
    'D2': 2.301442,
    'PPE': 0.284654
    } and returns parkinson(1) or not(0), 1->present , 0->not present"""

    query = ast.literal_eval(query)

    values = [float(value) for value in query.values()]

    # Convert the list of values to a numpy array and store it in 'test_value'
    test_value = np.array(values)
    sc = StandardScaler()

    lr_model = "models/parkinson/Parkinson_LR_model.pkl"

    with open(lr_model, 'rb') as file:
        LR_model = pickle.load(file)

    output = LR_model.predict(sc.fit_transform([test_value]))

    return "parkinson" + str(output)


def extract_dict(s):
    start = s.find("{")
    end = s.find("}") + 1
    dict_string = s[start:end]
    dictionary = ast.literal_eval(dict_string)
    return str(dictionary)


@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    print(body)
    input = body['message']

    output = parkinson(extract_dict(input))
    temp = ""

    for chunk in llm.stream("""Assist the user by replying appropriately ,If the test result is 1 , it indicates a likelihood of specified disease. 
        However, if the result is 0 , it suggests the absence of specified indicators., 
        disease test results:""" + str(output) + " Assistant:"):
        print(chunk, end="", flush=True)
        temp += chunk

    answer = {"content": temp}

    return {"output": answer}
