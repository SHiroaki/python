import random
data = [random.randint(-1000, 1000) for r in range(1000)]

# Without Map
result = []
for i in data:
  result.append(abs(i))

# Using a Map
result = list(map(abs, data))
