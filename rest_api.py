import json
import requests
import threading
import time
import torch
import traceback
from flask import Flask, request, render_template
from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained('gpt2-xl')
model = GPT2LMHeadModel.from_pretrained('gpt2-xl')

app = Flask(__name__)


def top_k_logits(logits, k):
    if k == 0:
        return logits
    values, _ = torch.topk(logits, k)
    min_values = values[:, -1]
    return torch.where(logits < min_values, torch.ones_like(logits, dtype=logits.dtype) * -1e10, logits)


@app.route("/generate", methods=['POST'])
def answer():
    # time.sleep(5000)
    sentence = ""
    try:
        # print("data:", request.form['data'], end=" - ")

        sentence = ''.join([x for x in request.form['data'] if ord(x) < 256])
        # print("---------------------------------------")
        sentence_split = sentence.split(" ")
        if "." not in sentence_split[len(sentence_split) - 1] or "!" not in sentence_split[
            len(sentence_split) - 1] or "?" not in sentence_split[len(sentence_split) - 1]:
            sentence = sentence + "?"

        tokenized = tokenizer.encode(sentence)

        sentence = tokenizer.decode(tokenized)

        if len(tokenized) > 450:
            return ""

        context = torch.LongTensor(tokenized).unsqueeze(dim=0)
        output = context
        prev = context

        temperature = 0.7
        top_k = 40

        model.eval()
        softmax = torch.nn.Softmax(dim=1)
        past = None
        end_tokens_q = "?"
        end_tokens_s = "!"
        end_tokens_p = "."
        current_token = ""
        counter = 0
        while counter < 100 and end_tokens_q not in current_token and end_tokens_s not in current_token and end_tokens_p not in current_token:
            counter += 1
            with torch.no_grad():
                logits, past = model.forward(prev, past=past)
            logits = logits[:, -1, :] / temperature
            logits = top_k_logits(logits, k=top_k)

            log_probs = softmax(logits)

            prev = torch.multinomial(log_probs, num_samples=1)
            current_token = prev[0][0].item()
            current_token = tokenizer.decode([current_token])
            output = torch.cat((output, prev), dim=1)
        ret = tokenizer.decode(output.squeeze().tolist())
        ret = ret.replace(sentence, "").replace("\n", "")

        return ret, 200

    except Exception:
        return "Hi, this is Gardian of the Bottexy, the First of His Name, The Unburnt, " \
               "King of the Humans, the Rhoynar and the First Men, King of Bytes, Khal of the Universe, " \
               "Protector of the Bot, Lady Regent of the Eight Kingdoms, Breaker of Chains and Father of Bots. " \
               "Please to not use characters that are too special", 400


@app.route("/", methods=['GET'])
def get_chat():
    return render_template(['index.html', "helper.js", "style.css"])


if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=True, host='0.0.0.0')
