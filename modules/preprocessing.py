import pandas as pd

def load_and_preprocess(file_path):
    """
    Load CSV file and preprocess logs
    """
    logs = pd.read_csv(file_path)
    logs['timestamp'] = pd.to_datetime(logs['timestamp'])
    logs['log_text'] = logs.apply(lambda x: f"{x['timestamp']} {x['user']} {x['ip']} {x['action']} {x['status']}", axis=1)
    logs['status_num'] = logs['status'].apply(lambda x: 1 if x in ['failed','suspicious'] else 0)
    return logs
