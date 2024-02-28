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
import json


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


@tool(return_direct=True)
def general_chat(query) -> str:
    """for answering general question/query/greeting for example hi,bye,what is cold etc"""
    query = str(query)
    answer = llm.invoke("keep it short and concise User:" + query)
    print(answer)
    return "casual mode:" + str(answer)


def detect_general(sentence):
    return "casual mode:" in sentence.lower()


tool_list = [parkinson, diabetes, general_chat]


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
    try:
        output = agent_executor.invoke(
            {"input": """use tool and tell if disease is present(1) or disease is not present(0) 
                Start: """ + body["message"]})
        if (detect_general(str(output['output']))):
            answer = llm.invoke(
                "Reply as it is: " + str(output['output']).replace("casual mode:content=", ""))

            return {"output": answer}
        answer = llm.invoke(
            """Assist the user by replying appropriately and short ,If the test result is 1/yes/present , it indicates a likelihood of specified disease. 
                    However, if the result is not 1/no/not present , it suggests the absence of specified indicators., 
                    disease test results:""" + str(output['output']) + " Assistant:")

        return {"output": answer}
    except TypeError:
        answer = llm.invoke("Reply to user that an Error Has Occured")
        return {"output": answer}
    # try:
    #     output = agent_executor.invoke(
    #         {"input": """use tool and tell if disease is present(1) or disease is not present(0)
    #          Start: """ + body["message"]})
    #     print(output)
    #     if (detect_general):
    #         answer = str(output['output']).replace("casual mode:content=", "")
    #         answer = {"output": {"content": answer,
    #                              "additional_kwargs": {}, "type": "ai", "example": False}}
    #         return {"output": answer}

    #     answer = llm.invoke(
    #         """Assist the user by replying appropriately and short ,If the test result is 1/yes/present , it indicates a likelihood of specified disease.
    #             However, if the result is not 1/no/not present , it suggests the absence of specified indicators.,
    #             disease test results:""" + str(output['output']) + " Assistant:")
    #     return {"output": answer}
    # except TypeError:
    #     answer = {"output": {"content": "there is an error",
    #                          "additional_kwargs": {}, "type": "ai", "example": False}}
    #     return {"output": answer}


# for chunk in agent_executor.stream({"input": "if you know answer no need to use tool just directly answer using Final Answer Q:what is machine learning write in 200 words?"}):
#     print(chunk, end='', flush=True)

# for chunk in llm.stream("what is an llm? write 200 words"):
#     print(chunk, end="", flush=True)
