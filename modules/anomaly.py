from sklearn.ensemble import IsolationForest

def detect_anomalies(logs):
    """
    Detect anomalies and assign severity
    """
    iso = IsolationForest(contamination=0.1, random_state=42)
    logs['anomaly'] = iso.fit_predict(logs[['status_num']])
    logs['severity'] = logs['anomaly'].map({1:'normal', -1:'critical'})
    return logs

