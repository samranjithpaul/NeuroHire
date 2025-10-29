import os
import pdfplumber
import csv
import requests
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
results = []

# 🔹 Use Ollama locally instead of OpenAI
# Make sure Ollama is running (`ollama serve`) and you’ve pulled a model, e.g. `ollama pull llama3.1`

def chat_gpt(conversation):
    # Combine the conversation into a single user prompt
    user_prompt = "\n".join([msg["content"] for msg in conversation if msg["role"] == "user"])

    # Send the request to the local Ollama server
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1",  # You can change this to mistral, phi3, etc.
                "prompt": user_prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"Error contacting Ollama: {str(e)}"


def pdf_to_text(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text


def update_csv(results):
    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Resume Name", "Comments", "Suitability"])
        csv_writer.writerows(results)


@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    global results
    if request.method == 'POST':
        resume_files = request.files.getlist('file[]')
        job_description = request.form.get('job_description', '').strip()
        mandatory_keywords = request.form.get('mandatory_keywords', '').strip()

        if not resume_files or not job_description or not mandatory_keywords:
            return jsonify({"error": "Please provide resume files, a job description, and mandatory keywords."}), 400

        results = []
        for resume_file in resume_files:
            filename = secure_filename(resume_file.filename)
            temp_path = os.path.join("/tmp", filename)
            resume_file.save(temp_path)

            resume_text = pdf_to_text(temp_path)
            os.remove(temp_path)

            conversation = [
                {"role": "system", "content": "You are a recruitment assistant that evaluates resumes."},
                {"role": "user", "content": f"Mandatory keywords: {mandatory_keywords}"},
                {"role": "user", "content": (
                    f"Job description: {job_description}\n\n"
                    f"Resume content: {resume_text}\n\n"
                    "Evaluate how suitable this candidate is for the job based on the resume and job description. "
                    "Explain reasoning briefly and end your response with one of the labels: "
                    "'Suitable', 'Not Suitable', or 'Maybe Suitable'. The label must be included at the end."
                )}
            ]

            response = chat_gpt(conversation)
            response_lower = response.lower()
            if "not suitable" in response_lower:
                suitability = "Not Suitable"
            elif "maybe suitable" in response_lower:
                suitability = "Maybe Suitable"
            else:
                suitability = "Suitable"

            results.append([filename, response, suitability])

        return jsonify({"results": results})

    return render_template('upload.html')


@app.route('/download_csv', methods=['GET'])
def download_csv():
    global results
    update_csv(results)
    return send_file('results.csv', as_attachment=True)


@app.route('/')
def index():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
