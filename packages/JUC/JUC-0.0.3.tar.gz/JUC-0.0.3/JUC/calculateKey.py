def calculate(key):
    return sum([ord(char) for char in key])

def getCString(text):
    values = text.split('.')
    return values[0], int(values[-1])