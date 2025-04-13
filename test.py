import requests
import random

def generate_random_input():
    return [
        random.randint(29, 77),
        random.choice([0, 1]),
        random.choice([0, 1, 2, 3]),
        random.randint(90, 180),
        random.randint(120, 600),
        random.choice([0, 1]),
        random.choice([0, 1, 2]),
        random.randint(70, 202),  
        random.choice([0, 1]),    
        round(random.uniform(0.0, 6.2), 1),  
        random.choice([0, 1, 2]),     
        random.choice([0, 1, 2, 3]),   
        random.choice([1, 2, 3])       
    ]

for i in range(1, 21):
    test_input = generate_random_input()
    
    try:
        response = requests.post("http://127.0.0.1:5000/predict", json={"features": test_input})
        result = response.json()

        if "error" in result:
            print(f"Test {i}: ERROR - {result['error']}")
        else:
            print(f"Test {i}:")
            print("  Input:", test_input)
            print("  Prediction:", "Heart Disease" if result["prediction"] == 1 else "No Heart Disease")
            if result.get("probability") != "Not available":
                print("  Probability:", result["probability"])
            print()

    except Exception as e:
        print(f"Test {i}: Exception occurred - {e}")
