import openai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)


@app.route('/', methods=['GET','POST'])
def get_page():
    if request.method == 'POST':
        user_input = request.form['user_input']
        openai.api_key = os.environ.get("API_TOKEN")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_input,
            max_tokens=2000,
            temperature=0
        )
        result = response["choices"][0]["text"]
        return render_template("index.html", ai_answer=result)
    return render_template("index.html")


@app.route('/imagecreator', methods=['GET','POST'])
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



