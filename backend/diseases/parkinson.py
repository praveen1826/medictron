from langchain.agents import tool
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import ast


class Parkinson():

    @tool
    def parkinson(query: str) -> str:
        """Takes in a dictionary of key value pairs in this order {
        'MDVP:Fo(Hz)': 119.99200,
        'MDVP:Fhi(Hz)': 157.30200,
        'MDVP:Flo(Hz)': 74.99700,
        'MDVP:Jitter(%)': 0.00784,
        'MDVP:Jitter(Abs)': 0.00007,
        'MDVP:RAP': 0.00370,
        'MDVP:PPQ': 0.00554,
        'Jitter:DDP': 0.01109,
        'MDVP:Shimmer': 0.04374,
        'MDVP:Shimmer(dB)': 0.42600,
        'Shimmer:APQ3': 0.02182,
        'Shimmer:APQ5': 0.03130,
        'MDVP:APQ': 0.02971,
        'Shimmer:DDA': 0.06545,
        'NHR': 0.02211,
        'HNR': 21.03300,
        'RPDE': 0.414783,
        'DFA': 0.815285,
        'spread1': -4.813031,
        'spread2': 0.266482,
        'D2': 2.301442,
        'PPE': 0.284654
        } and returns parkinson(1) or not(0)"""

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
