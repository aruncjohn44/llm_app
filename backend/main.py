from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Load your OpenAI API key here
openai.api_key = 'your-openai-api-key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data['prompt']
    temperature = float(data['temperature'])
    model = data['model']

    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=150
        )
        result = response.choices[0].text.strip()

        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
