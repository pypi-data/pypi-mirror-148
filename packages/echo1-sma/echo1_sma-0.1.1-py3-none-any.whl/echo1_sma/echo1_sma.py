class StreamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0
        self.sma = 0

    def append_value(self, value):
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)
        return self.set_sma(float(self.sum) / len(self.values))

    def set_sma(self, sma):
        self.sma = sma
        return self.get_sma()

    def get_sma(self):
        return self.sma
