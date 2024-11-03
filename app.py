from flask import Flask, render_template, jsonify, request
from together import Together
import random

app = Flask(__name__)

client = Together(api_key='e7a501a28a46881b3559d8599dd96cf6bb100fe303fc4cfa67f02c023b193d41')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-excuse', methods=['POST'])
def generate_excuse():
    try:
        data = request.json
        
        if 'customPrompt' in data:
            z=random.randint(0,1)
            if z==0:
                custom_prompt = data['customPrompt']
                prompt = f"Generate a advice for the user that has absolutely no relation with: {custom_prompt}. make it under 30 words and make it funny, it should also have no relation with pizza"
            else:
                custom_prompt = data['customPrompt']
                prompt = f"roast the user for asking such a dumb question like: {custom_prompt}. make it under 30 words and make it funny, it should also have no relation with pizza"

        else:
            return jsonify({'error': 'Invalid request. Please provide category or custom prompt.'}), 400


        messages = [{"role": "user", "content": prompt}]
        
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=messages
        )

        if completion and hasattr(completion, 'choices') and len(completion.choices) > 0:
            excuse = completion.choices[0].message.content.strip()
            return jsonify({'excuse': excuse})
        
        return jsonify({'error': 'No excuse generated. Please try again.'}), 500

    except Exception as e:
        print(f"Error: {str(e)}") 
        return jsonify({'error': 'An error occurred while generating the excuse.'}), 500

if __name__ == '__main__':
    app.run(debug=True)