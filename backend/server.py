from dotenv import load_dotenv
# from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
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

llm = ChatGoogleGenerativeAI(model="gemini-pro", streaming=True)

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/react")

parkinson = Parkinson().parkinson
diabetes = Diabetes().diabetes


tool_list = [parkinson, diabetes]


agent = create_react_agent(llm, tool_list, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent,
                               tools=tool_list,
                               #    return_intermediate_steps=True,
                               handle_parsing_errors=True,
                               max_iterations=5,
                               verbose=True
                               )

# output = agent_executor.invoke(
#     {"input": "if you know answer no need to use tool just directly answer using Final Answer Q:what is an llm?"})


# class Item(BaseModel):
#     output: str


@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    print(body)
    output = agent_executor.invoke(
        {"input": "use tool and tell if disease is present or disease is not present" + body["message"]})
    print(output)
    answer = llm.invoke(
        """Assist the user by replying appropriately ,If the test result is 1/yes/present , it indicates a likelihood of specified disease. 
        However, if the result is not 1/no/not present , it suggests the absence of specified indicators., 
        disease test results:""" + str(output['output']) + " Assistant:")
    return {"output": answer}

# for chunk in agent_executor.stream({"input": "if you know answer no need to use tool just directly answer using Final Answer Q:what is machine learning write in 200 words?"}):
#     print(chunk, end='', flush=True)

# for chunk in llm.stream("what is an llm? write 200 words"):
#     print(chunk, end="", flush=True)
