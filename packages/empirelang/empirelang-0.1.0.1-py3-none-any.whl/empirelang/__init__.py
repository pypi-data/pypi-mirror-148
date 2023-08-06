__version__ = '0.1.0.1'
class Empire:
  def __init__(self, version="0.1.0b"):
    self.version = version
  def test(self):
    print("self")
  class system:
    def version(self):
      return "v" + self.version
  class vars:
    def __init__(self):
      self.names = []
      self.values = []
    def create(self, name, value):
      self.names.append(name)
      self.values.append(value)
    def get(self, name):
      return self.value[self.name.index(name)]
    def set(self, name, value):
      if name in self.names:
        self.values[self.names.index(name)] = value
        return 0
      else:
        raise Exception("ERROR")
    def change(self, name, value):
      if name in self.names:
        self.values[self.names.index(name)] += value
      else:
        raise Exception("ERROR")
    def delete(self, name):
      del self.values[self.names.index(name)]
      del self.names[self.names.index(name)]
      return 0
  class operators:
    def __init__(self):
      pass
    def add(self, a, b):
      return a + b
    def subtract(self, a, b):
      return a - b
    def multiply(self, a, b):
      return a * b
    def divide(self, a, b):
      return a / b
    def floorDivide(self, a, b):
      return a // b
    def modulo(self, a, b):
      return a % b
  class data:
    def __init__(self, data):
      if not type(data) is list:
        data = list(data)
      self.data = data
    def toInt(data):
      for i in range(len(data)):
        data[i] = int(data[i])
      return data
    def mean(data):
      if not type(data) is list:
        return
      else:
        sum = 0
        data = toInt(data)
        for i in range(len(data)):
          sum += data[i]
        return sum / len(data)
    def median(data):
      if not type(data) is list:
        return
      else:
        data = toInt(data)
        data.sort()
        if len(data) % 2 == 0:
          low = data[int(len(data) / 2 - 1)]
          high = data[int(len(data) / 2)]
          return mean([low, high])
        else:
          return data[int(len(data) / 2)]
    def mode(data):
      if not type(data) is list:
        return
      else:
        data = toInt(data)
        data.sort()
        # Finish mode
  class console:
    def __init__(self):
      pass
    def log(self, output):
      print(output)
    def prompt(self, prompt):
      return input(prompt)
    def logf(self, output, data):
      msg = output
      for i in range(len(msg) // 3):
        msg = msg.replace("{" + i + "}", data[i])