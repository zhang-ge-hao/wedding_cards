import os
import json
import hashlib
import shutil


with open(os.path.join("personal_data", "description.jsonl"), encoding="utf-8") as fin:
    description_data = "".join(fin.readlines())

description_data = [json.loads(line) for line in description_data.split("\n")]
nick_2_hash = {ld["花名"]: hashlib.md5(ld["花名"].encode()).hexdigest() for ld in description_data}

if os.path.exists("wedding_cards_anonymous"):
    shutil.rmtree("wedding_cards_anonymous")
shutil.copytree("wedding_cards", "wedding_cards_anonymous")

for dir_name in os.listdir("wedding_cards_anonymous"):
    hash_str = nick_2_hash[dir_name]
    src_dir = os.path.join("wedding_cards_anonymous", dir_name)
    dst_dir = os.path.join("wedding_cards_anonymous", hash_str)
    shutil.move(src_dir, dst_dir)