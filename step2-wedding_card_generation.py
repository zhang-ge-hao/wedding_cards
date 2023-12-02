import json
import base64
import requests
import os
from tqdm import tqdm


with open(os.path.join("personal_data", "Authorization"), encoding="utf-8") as fin:
    authorization = fin.readline().strip()

with open(os.path.join("personal_data", "original.jsonl"), encoding="utf-8") as fin:
    ori_data = "".join(fin.readlines())

with open(os.path.join("personal_data", "description.jsonl"), encoding="utf-8") as fin:
    description_data = "".join(fin.readlines())

ori_data = [json.loads(line) for line in ori_data.split("\n")]
description_data = [json.loads(line) for line in description_data.split("\n")]
assert len(ori_data) == len(description_data) and all(all(oi[k] == di[k] for k in oi.keys()) for oi, di in zip(ori_data, description_data))

url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": authorization,
}

for item in tqdm(description_data):
    body = {
    "steps": 40,
    "width": 1024,
    "height": 1024,
    "seed": 0,
    "cfg_scale": 5,
    "samples": 10,
    "style_preset": "analog-film",
    "text_prompts": [
        {
            "text": item["画面描述"],
            "weight": 1
        }
    ],
    }

    response = requests.post(
        url,
        headers=headers,
        json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    output_dir = os.path.join("wedding_cards", item["花名"])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, image in enumerate(data["artifacts"]):
        with open(os.path.join(output_dir, "%d.png" % i), "wb") as f:
            f.write(base64.b64decode(image["base64"]))