from PIL import Image, ImageDraw, ImageFont
import os
import json
import qrcode
from tqdm import tqdm
import hashlib


def generate_qrcode(url, bg_color, fg_color, save_path):
    # 创建QRCode实例
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 将URL添加到QRCode中
    qr.add_data(url)
    qr.make(fit=True)

    # 创建QRCode图像
    img = qr.make_image(fill_color=fg_color, back_color=bg_color)

    # 保存图像
    img.save(save_path)


def get_average_rgb(image):
    # 获取图像的所有像素数据
    pixels = list(image.getdata())

    # 计算每个通道的累计值
    total_red = 0
    total_green = 0
    total_blue = 0

    for pixel in pixels:
        total_red += pixel[0]
        total_green += pixel[1]
        total_blue += pixel[2]

    # 计算平均值
    num_pixels = len(pixels)
    average_red = total_red // num_pixels
    average_green = total_green // num_pixels
    average_blue = total_blue // num_pixels

    return average_red, average_green, average_blue


def get_contrast_color(background_color):
    # 计算相对亮度
    relative_luminance = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255

    # 根据亮度值确定文字颜色
    if relative_luminance > 0.5:
        text_color = (0, 0, 0)  # 黑色文字
    else:
        text_color = (255, 255, 255)  # 白色文字

    return text_color


def create_greeting_card(data):

    output_dir = os.path.join("wedding_cards_final", data["花名"])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image_path = os.path.join("wedding_cards", data["花名"], "picked.png")
    front_output_path = os.path.join(output_dir, "front.png")
    back_output_path = os.path.join(output_dir, "back.png")
    qrcode_output_path = os.path.join(output_dir, "qrcode.png")

    # title_text = "\n".join([c1 + c2 for c1, c2 in zip("我们结婚了", "也祝您幸福")])
    title_text = "%s\n敬启" % data["花名"]
    content_text = """尊敬的 %s：


我是张格皓，我最近结婚了。
我代表我和我的妻子，向您在我过往的工作和生活中给我的支持和帮助，表达我们最诚挚的感谢。
在这段我比较幸福的日子里，衷心地希望您也可以幸福。
祝大家都有美好的一天。


张格皓
二零二三年十二月二日""" % data["花名"]
    comment_text = """* 贺卡的封面图片，是由人工智能（ChatGPT + 
StabilityAI），以您的花名或者姓名为灵感，生
成的专属于您的图片。您可以扫描二维码，获取为
您生成的所有图片。"""

    image = Image.open(image_path)
    background_color = get_average_rgb(image)  # 设置背景色
    font_color = get_contrast_color(background_color)  # 设置前景色

    # 生成二维码
    url_root = "https://github.com/zhang-ge-hao/wedding_cards/tree/master/wedding_cards_anonymous/"
    url = "%s%s" % (url_root, hashlib.md5(data["花名"].encode()).hexdigest())
    generate_qrcode(url, background_color, font_color, qrcode_output_path)

    # 创建一个纯色背景图片
    width, height = 2480, 3490  # 设置图片大小
    background = Image.new("RGB", (width, height), background_color)

    # 调整配图大小，你可能需要根据需要进行更复杂的调整
    image = image.resize((1754, 1754))
    background.paste(image, (0, 1754))

    # 添加文字
    draw = ImageDraw.Draw(background)
    # 加载中文字体，你可以替换成你自己的字体文件路径
    font_path = "nzgrRuYinZouZhangKai.ttf"
    font = ImageFont.truetype(font_path, size=363)
    
    text_bbox = draw.textbbox((726, 1754), title_text, font=font)
    
    # 根据文本边界框信息调整文本位置
    text_position = (1754, 1754 + 10 + 30)
    draw.text(text_position, title_text, font=font, fill=font_color)

    # 工位
    font_path = "DreamHanSerifCN-W20.ttf"
    font = ImageFont.truetype(font_path, size=30)
    draw = ImageDraw.Draw(background)        
    text_position = (1754 + 40, 1754 + 10)
    draw.text(text_position, data["办公地点"], font=font, fill=font_color)

    # 保存最终图片
    background.save(front_output_path)

    # 开始生成背面
    current_h, pad, font_size, font_size_comment, char_per_line = 200, 150, 100, 50, 20
    # 创建一个纯色背景图片
    width, height = 2480, 3490  # 设置图片大小
    background = Image.new("RGB", (width, height), background_color)
    # 加载中文字体，你可以替换成你自己的字体文件路径
    font_path = "nzgrRuYinZouZhangKai.ttf"
    font = ImageFont.truetype(font_path, size=font_size)

    ori_lines = content_text.split("\n")
    processed_lines = []
    row = 0
    while row < len(ori_lines):
        processed_line = ori_lines[row][: char_per_line]
        ori_lines[row] = ori_lines[row][char_per_line: ]
        if len(ori_lines[row]) == 0:
            row += 1
            is_paragraph = True
        else:
            is_paragraph = False
        processed_lines.append((processed_line, is_paragraph))

    for line, is_paragraph in processed_lines:
        # 添加文字
        draw = ImageDraw.Draw(background)        
        # 根据文本边界框信息调整文本位置
        text_position = (1240 - font_size * len(line) // 2, current_h)
        draw.text(text_position, line, font=font, fill=font_color)
        current_h += pad if is_paragraph else font_size
    
    # 下方备注
    font_path = "DreamHanSerifCN-W20.ttf"
    font = ImageFont.truetype(font_path, size=font_size_comment)
    draw = ImageDraw.Draw(background)
    text_position = (200, current_h + pad * 4)
    draw.text(text_position, comment_text, font=font, fill=font_color)

    # 下方二维码
    image = Image.open(qrcode_output_path)
    image = image.resize((450, 450))
    background.paste(image, (1650, 2650))
    os.remove(qrcode_output_path)

    background.save(back_output_path)


if __name__ == "__main__":
    with open(os.path.join("personal_data", "description.jsonl"), encoding="utf-8") as fin:
        description_data = "".join(fin.readlines())
    description_data = [json.loads(line) for line in description_data.split("\n")]
    for data in tqdm(description_data):
        create_greeting_card(data)