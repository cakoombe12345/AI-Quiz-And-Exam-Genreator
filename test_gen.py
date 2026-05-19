from ai_engine import generate_quiz
import os

api_key = "AIzaSyDzmaiGlQA_OGuk-CVpkG7IJF96lg1be1g"
context = "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability."

print("Testing generate_quiz...")
try:
    quiz = generate_quiz(api_key, context, "Easy", ["Multiple Choice"], 2)
    if quiz:
        print("Success!")
        print(quiz)
    else:
        print("Failed, returned None")
except Exception as e:
    print(f"Exception: {e}")
