import requests

headers = {
    'accept': 'application/json',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.studocu.com',
    'priority': 'u=1, i',
    'referer': 'https://www.studocu.com/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-forwarded-for': '105.37.78.202, 172.71.115.74, 172.71.115.74',
    'x-request-id': '8294f6f7-603b-4598-9097-aa40d920de2d',
    'x-session-id': '479ecfe8-ec70-47cc-aa87-8019fca4e56d',
}

json_data = {
    'text': "Respiratory Failure",
}

response = requests.post('https://api.studocu.com/rest-api/v1/quizzes/v0/draft-quiz-questions', headers=headers, json=json_data)
print(response.json())
