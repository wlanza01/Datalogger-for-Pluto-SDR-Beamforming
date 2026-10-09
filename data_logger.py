import csv
import os
from datetime import datetime


class DataLogger:
    def __init__(self, filename):
        self.filename = filename
        self.file_exists = os.path.exists(filename)

    def log(self, **kwargs):
        fieldnames = list(kwargs.keys())

        with open(self.filename, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=["timestamp"] + fieldnames)

            if not self.file_exists:  # Only write header on first write
                writer.writeheader()
                self.file_exists = True  # Track that we've written it

            row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            row.update(kwargs)
            writer.writerow(row)