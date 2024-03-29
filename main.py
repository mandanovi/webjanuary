import openai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def get_page():
    if request.method == 'POST':
        user_input = request.form['user_input']
        session['user_question'] = user_input
        openai.api_key = os.environ.get("API_TOKEN")
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": session['user_question']},
            {"role": "assistant", "content": session.get('assistant_answer', '')},
            {"role": "user", "content": user_input}])
        result = response["choices"][0]["message"]["content"]
        session['assistant_answer'] = result
        session.modified = True
        new_result = result.split('\n')
        return render_template("index.html", ai_answer=new_result)
    session['assistant_answer'] = ''
    return render_template("index.html")


@app.route('/imagecreator', methods=['GET', 'POST'])
def get_image():
    if request.method == 'POST':
        image_input = request.form['image_input']
        openai.api_key = os.environ.get("API_TOKEN")
        response = openai.Image.create(
          prompt=image_input,
          n=1,
          size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return render_template("image.html", ai_image=image_url)
    return render_template("image.html")


if __name__ == "__main__":
    app.run(debug=True)
