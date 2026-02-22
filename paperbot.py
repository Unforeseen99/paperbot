import time
import random

print("Paperbot started...")

while True:
    price = random.uniform(0.98, 1.02)
    print(f"Monitoring market... simulated price: {price}")
    time.sleep(10)