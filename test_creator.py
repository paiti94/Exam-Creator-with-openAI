import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()
client = OpenAI()
class TestGenerator:

    def __init__(self, topic, num_possible_answers, num_questions):
        self.topic = topic
        self.num_possible_answers = num_possible_answers
        self.num_questions = num_questions

        if self.num_questions > 6:
            raise ValueError("Attention! Generation of many questions might be expensive!")
        if self.num_possible_answers > 5:
            raise ValueError("More than 5 possible answers is not supported!")

    def run(self):
        prompt = self.create_prompt()
        if TestGenerator._verify_prompt(prompt):
            response = self.generate_quiz(prompt)
            return response.choices[0]

        else: raise ValueError("Prompt not accepted.")

    def generate_quiz(self, prompt):
        response = client.completions.create(model='davinci-002',
                                             prompt=prompt,
                                             max_tokens=256,
                                             temperature=0.7,
                                              )
        return response


    @staticmethod
    def _verify_prompt(prompt):
        print(prompt)
        response = input("Are you happy with the prompt? (y/n)")

        if response.upper() == "Y":
            return True
        return False


    def create_prompt(self):
        prompt = f"Create a multiple choice quiz on the topic of {self.topic} consisting of {self.num_questions} questions."\
        +f"Each question should have {self.num_possible_answers} options."\
        +f"Also include the correct answer for each question using the starting string 'Correct Answer: '."

        return prompt

if __name__ == "__main__":
    gen = TestGenerator("Korea History", 4, 2)
    response = gen.run()
    print(response)