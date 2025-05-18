import requests

url = 'http://localhost:5000/submit'
data = {"problem_id": 1, "code": "print(1)"}

response = requests.post(url, json=data)
print(response.json())