import numpy as np

RPS_PER_SERVER = 20000
SERVER_COST = 300
SAFETY_BUFFER = 0.30

def calculate_servers(preds):

    preds = np.array(preds)

    rps_buffer = preds * (1 + SAFETY_BUFFER)

    servers = np.ceil(rps_buffer / RPS_PER_SERVER)
    cost = servers * SERVER_COST

    return servers, cost
