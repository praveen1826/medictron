from dotenv import load_dotenv
from langchain_community.llms.llamacpp import LlamaCpp
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.globals import set_debug
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import ast


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows CORS for your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

set_debug(True)


llm = LlamaCpp(
    model_path=r"C:\Users\thiru\Documents\apps\ai_models\Gen_AI\Text_Gen\mistral-7b-v0.1.Q8_0.gguf",
    temperature=0.75,
    max_tokens=50,
    top_p=1,
    verbose=True,
)

template = """Assist the user by replying appropriately ,
        If the test result is 1 , it indicates a likelihood of specified disease. 
        However, if the result is 0 , it suggests the absence of specified indicators., 
        disease test results: {output} " Assistant:"""

prompt = ChatPromptTemplate.from_template(template=template)


chain = prompt | llm.bind(
    stop=["User:", "Human:", "Assistant:", "Assistant: ", "\n"]) | StrOutputParser()


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

    return "parkinson = " + str(output)


def diabetes(query: str) -> str:
    """Takes in a dictionary of key value pairs in this order {
        'Pregnancies': 6,
        'Glucose': 148,
        'BloodPressure': 72,
        'SkinThickness': 35,
        'Insulin': 0,
        'BMI': 33.6,
        'DiabetesPedigreeFunction': 0.627,
        'Age': 50
        } and returns diabetes(1) or not(0)"""

    query = ast.literal_eval(query)

    values = [float(value) for value in query.values()]

    # Convert the list of values to a numpy array and store it in 'test_value'
    test_value = np.array(values)
    sc = StandardScaler()

    best_model = "models/diabetes/Diabetes_AdaBoostClassifier_model.pkl"

    with open(best_model, 'rb') as file:
        Best_model = pickle.load(file)

    output = Best_model.predict(sc.fit_transform([test_value]))

    return "diabetes = " + str(output)


def extract_dict(s):
    start = s.find("{")
    end = s.find("}") + 1
    dict_string = s[start:end]
    dictionary = ast.literal_eval(dict_string)
    return str(dictionary)


def contains_parkinson(sentence):
    return "parkinson" in sentence.lower()


def contains_diabetes(sentence):
    return "diabetes" in sentence.lower()


@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    print(body)
    input = body['message']

    if (contains_parkinson(input)):
        output = parkinson(extract_dict(input))

    elif (contains_diabetes(input)):
        output = diabetes(extract_dict(input))

    else:
        try:
            output = diabetes(extract_dict(input))
        except ValueError:
            output = parkinson(extract_dict(input))

    temp = ""

    for chunk in chain.stream({"output": str(output)}):
        print(chunk, end="", flush=True)
        temp += chunk

    answer = {"content": temp}

    return {"output": answer}
