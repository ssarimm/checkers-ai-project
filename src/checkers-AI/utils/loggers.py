import csv
from datetime import datetime

class Logger:
    def __init__(self, filename="data/game_logs.csv"):
        self.filename = filename
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'state', 'action', 'reward'])

    def log(self, state, action, reward):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), state.tolist(), action, reward])