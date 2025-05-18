import requests

class MCQGeneratorAPI:
    def __init__(self):
        self.headers = {
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
        self.api_url = 'https://api.studocu.com/rest-api/v1/quizzes/v0/draft-quiz-questions'

    def generate_questions(self, text):
        """
        Generate MCQ questions from the provided text.
        
        Args:
            text (str): The text to generate questions from
            
        Returns:
            tuple: (success, data/error_message)
            - success (bool): Whether the request was successful
            - data (dict): The response data if successful
            - error_message (str): Error message if unsuccessful
        """
        try:
            json_data = {'text': text}
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=json_data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if isinstance(response_data, dict) and 'data' in response_data:
                    return True, response_data['data']
                return False, "The API response format was unexpected."
            return False, f"API request failed with status code: {response.status_code}"
            
        except requests.RequestException as e:
            return False, f"Network error: {str(e)}"
        except ValueError as e:
            return False, f"Error parsing response: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def filter_questions_by_difficulty(self, questions, difficulty):
        """
        Filter questions by difficulty level.
        
        Args:
            questions (list): List of question dictionaries
            difficulty (str): Difficulty level to filter by ('easy', 'medium', 'hard', 'all')
            
        Returns:
            list: Filtered questions
        """
        if difficulty == 'all':
            return questions
        return [q for q in questions if q.get('difficulty', '').upper() == difficulty.upper()]

    def group_questions_by_difficulty(self, questions):
        """
        Group questions by their difficulty level.
        
        Args:
            questions (list): List of question dictionaries
            
        Returns:
            dict: Questions grouped by difficulty
        """
        questions_by_difficulty = {}
        for question in questions:
            diff = question.get('difficulty', 'UNKNOWN')
            if diff not in questions_by_difficulty:
                questions_by_difficulty[diff] = []
            questions_by_difficulty[diff].append(question)
        return questions_by_difficulty 