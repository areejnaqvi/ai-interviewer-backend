from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/generate_questions', methods=['POST', 'OPTIONS'])
def generate_questions():
    if request.method == 'OPTIONS':
        # CORS preflight request
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
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

@app.route('/process_response', methods=['POST'])
def process_response():
    data = request.json
    user_response = data.get('response')

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI Interviewer"},
            {"role": "user", "content": f"Given the response: {user_response}, provide follow-up questions if necessary."}
        ],
        max_tokens=150
    )

    follow_up_questions = response.choices[0].message.content.strip().split('\n')
    return jsonify(followUpQuestions=follow_up_questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
