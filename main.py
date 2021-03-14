from flask import Flask, render_template, request
import openai
import os


# Before running you need to have your API key
# (see: https://beta.openai.com/docs/developer-quickstart)
# set in this environment variable.
#
# export OPENAI_API_KEY="sk-yourkey"
#
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


def get_prompt(user_inputs):
    # TODO: produce a good prompt
    # e.g.
    # ["Batman", "robots", "Great Depression"] ->
    # "Let me tell you a story about Batman, robots and Great Depression. It"
    return "Let me tell you a story about {} and {}. It".format(", ".join(user_inputs[:-1]),
                                                                user_inputs[-1])


def ask(user_inputs):
    prompt_text = get_prompt(user_inputs)

    # TODO: review these parameter values
    response = openai.Completion.create(engine="davinci",
                                        prompt=prompt_text,
                                        temperature=0.8,
                                        max_tokens=800,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0.3,
                                        stop=["\n"])
    story = prompt_text + response["choices"][0]["text"]
    return story


@app.route("/", methods=["GET", "POST"])
def show_form():

    if request.method == "GET":
        return render_template("user_form.html")

    user_input = request.form.get("user_input")
    user_input = [txt.strip() for txt in user_input.split(",")]

    answer = ask(user_input)

    return answer


if __name__ == "__main__":
    app.run(debug=True)
