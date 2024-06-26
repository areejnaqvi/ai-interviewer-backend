from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from openai import OpenAI

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
CORS(app=app)

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
# openai.api_key = 'sk-proj-YvIKcI04adywfT3JtVQpT3BlbkFJy1cyTQqTEetYR2FMVyDi'

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    if request.method == 'OPTIONS':
        # CORS preflight request
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Methods'] = 'POST'
        headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    if request.method == 'POST':
        data = request.json
        job_listing = data.get('job_listing')

        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI Interviewer"},
                {"role": "user", "content": f"Generate interview questions for the following job listing: {job_listing}"}
            ],
            max_tokens=150
        )
        questions = response.choices[0].message.content.strip().split('\n')
        return jsonify(questions=questions, status=200, ok=True)


@app.route('/ask_followup', methods=['POST'])
def ask_followup():
    data = request.json
    transcript = data.get('transcript')
    question = data.get('question')

    client = OpenAI(api_key='sk-proj-YvIKcI04adywfT3JtVQpT3BlbkFJy1cyTQqTEetYR2FMVyDi')

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI Interviewer"},
            {"role": "user", "content": f"I asked the interviewee the following question: {question}. There response was ${transcript}. Can you generate one followup question from this transcript, but only if it is pertinent. Otherwise simply say no followups (in those exact terms)"}
        ],
        max_tokens=150
    )
    question = response.choices[0].message.content.strip().split('\n')
    print(f"followup question is {question}")
    return jsonify(questions=question[0], status=200, ok=True)


@app.route('/analyze_responses', methods=['POST'])
def analyze_responses():
    data = request.json
    responses = data.get('responses')

    client = OpenAI()

    analyzed_data = {}  
    for question, response in responses.items():
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI Interviewer"},
                {"role": "user", "content": f"I asked my interviewee the following question: {question}\nThere response is as follows: {response}. Please give feedback on this response as an AI Interviewer and rate it out of 10."}
            ],
            max_tokens=150
        )

        analyzed_data[question] = {
            'response': response.choices[0].message.content.strip()
        }

    feedback = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI Interviewer"},
            {"role": "user", "content": f"Based on the following feedback for various questions answered by the interviewee, can you provide an analysis on whether the interviewee is a good fit for this role? The feedback is as follows: {analyzed_data}"}
        ]
    )

    feedbackText = feedback.choices[0].message.content.strip()
    print(f'analyzed data is {analyzed_data} and feedback is {feedbackText}')

    return jsonify(feedback=feedbackText)

if __name__ == '__main__':
    app.run(debug=True)
