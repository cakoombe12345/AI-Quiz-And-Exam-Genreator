from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
import json

class Question(BaseModel):
    type: str = Field(description="One of: 'mcq', 'short_answer', 'true_false'")
    question_text: str = Field(description="The actual question to ask")
    options: Optional[List[str]] = Field(description="List of 4 options if the type is 'mcq', otherwise null or empty list")
    correct_answer: str = Field(description="The correct answer. If 'mcq', it should exactly match one of the options. If 'true_false', it should be 'True' or 'False'.")
    explanation: str = Field(description="Explanation of why the answer is correct")

class Quiz(BaseModel):
    questions: List[Question]

def generate_quiz(api_key: str, context_text: str, difficulty: str, question_types: List[str], num_questions: int) -> Optional[Quiz]:
    """Generates a quiz using the new Google GenAI API."""
    try:
        # Initialize client with the new SDK
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert educational AI. Generate a quiz based on the following material.
        
        Constraints:
        - Difficulty level: {difficulty}
        - Total number of questions: {num_questions}
        - Included question types: {', '.join(question_types)}
        
        Material / Context to base the questions on:
        ```
        {context_text}
        ```
        
        Return the result strictly as a valid JSON object adhering to the specified schema.
        Ensure that for MCQ questions, the `correct_answer` matches exactly one of the strings in the `options` list.
        """
        
        # Using the gemini-3-flash-preview model per the user's snippet
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Quiz
            )
        )
        
        # Load the structured JSON response
        quiz_data = json.loads(response.text)
        return Quiz(**quiz_data)
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return None
