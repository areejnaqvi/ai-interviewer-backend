# AI Interviewer Backend

Welcome to the backend repository for AI Interviewer, a web application designed to facilitate AI-driven interviews.

## Overview

AI Interviewer Backend serves as the server-side component for handling interview-related functionalities. It manages initial and follow up interview question generation, interviewee responses capturing, AI analysis of responses, and feedback delivery.


## Technologies Used

- **Python**: Backend language for business logic and API development.
- **OpenAI API**: Integration for AI-based interview question generation and analysis.


## API Endpoints

- POST /generate-questions: Generates interview questions based on the job title/listing provided as input
- POST /ask_followup: Generate follow up questions based on the response provided by the interviee for a particular question asked by the AI interviewer
- POST /analyze_responses: Analyze the interviewee's responses to each question individually and as a whole in order to provide feedback on the interview


## Installation

To run the backend locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd ai-interviewer-backend
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Add env variables**:
   Create a .env file and add OPENAI_API_KEY. The value for this variable is provided in the presentation slides.
4.  Run the application. Note that the backend must run on port 5000 and the frontend must run on port 4200
  ```bash
  python app.py
