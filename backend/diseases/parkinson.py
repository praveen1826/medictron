from langchain.agents import tool
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import ast


class Parkinson():

    @tool(return_direct=True)
    def parkinson(query: str) -> str:
        """Takes in a dictionary of key value pairs in this order {
        'MDVP:Fo(Hz)': 119.99200,
        'MDVP:Fhi(Hz)': 157.30200,
        'MDVP:Flo(Hz)': 74.99700,
        'MDVP:Jitter(%)': 0.00784,
        ....
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

        return "parkinson =" + str(output)
