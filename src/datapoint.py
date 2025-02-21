import datetime

class UnProcessedDataPoint:
    def __init__(self, date: int, stage: float):
        self.date = date
        self.stage = stage

class ProcessedDataPoint:
    def __init__(self, date: int, stage: float):
        self.date = date
        self.stage = stage

    def __str__(self):
        return f"Stage: {self.stage}, Predicted at {self.date.strftime('%m/%d/%Y %I:%M %p')}"
        