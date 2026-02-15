import numpy as np

RPS_PER_SERVER = 5000
SERVER_COST = 300

def calculate_servers(preds):
    servers = np.ceil(np.array(preds) / RPS_PER_SERVER)
    cost = servers * SERVER_COST
    return servers, cost
