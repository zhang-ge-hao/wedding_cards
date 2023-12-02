import os
import json
import hashlib
import shutil


if os.path.exists("wedding_cards_anonymous"):
    shutil.rmtree("wedding_cards_anonymous")
shutil.copytree("wedding_cards", "wedding_cards_anonymous")

for dir_name in os.listdir("wedding_cards_anonymous"):
    hash_str = hashlib.md5(dir_name.encode()).hexdigest()
    src_dir = os.path.join("wedding_cards_anonymous", dir_name)
    dst_dir = os.path.join("wedding_cards_anonymous", hash_str)
    shutil.move(src_dir, dst_dir)