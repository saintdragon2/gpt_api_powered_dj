import os
from PIL import Image, ImageDraw, ImageFont

def add_text_border(draw, text, position, font, fill, border_width, border_color):
    x, y = position
    for x_offset in range(-border_width, border_width + 1):
        for y_offset in range(-border_width, border_width + 1):
            draw.text((x + x_offset, y + y_offset), text, font=font, fill=border_color)
    draw.text(position, text, font=font, fill=fill)

def create_album_art(image_path, title, artist):
    img = Image.open(image_path)
    width, height = img.size
    draw = ImageDraw.Draw(img)

    title_font_size = int(height * 0.07)
    artist_font_size = int(height * 0.05)
    # 폰트 설정
    title_font = ImageFont.truetype("malgun.ttf", title_font_size)
    artist_font = ImageFont.truetype("malgun.ttf", artist_font_size)
    # 맥
    # title_font = ImageFont.truetype("/Library/Fonts/Supplemental/AppleGothic.ttf", title_font_size)
    # artist_font = ImageFont.truetype("/Library/Fonts/Supplemental/AppleGothic.ttf", artist_font_size)


    text_color = (255, 255, 255)
    border_color = (0, 0, 0)
    border_width = 15

    title_width, title_height = draw.textlength(title, font=title_font), title_font.getbbox(title)[1]
    while title_width > width * 0.9:
        title_font_size -= 1
        artist_font_size = int(title_font_size * 0.7)
        
        title_font = ImageFont.truetype("malgun.ttf", title_font_size)
        artist_font = ImageFont.truetype("malgun.ttf", artist_font_size)
        # title_font = ImageFont.truetype("/Library/Fonts/Supplemental/AppleGothic.ttf", title_font_size)
        # artist_font = ImageFont.truetype("/Library/Fonts/Supplemental/AppleGothic.ttf", artist_font_size)
        title_width, title_height = draw.textlength(title, font=title_font), title_font.getbbox(title)[1]

    title_x = (width - title_width) / 2
    title_y = (height - title_height) * 0.75

    artist_width, artist_height = draw.textlength(artist, font=artist_font), artist_font.getbbox(artist)[1]
    artist_x = (width - artist_width) / 2
    artist_y = title_y + title_font_size + 20

    add_text_border(draw, title, (title_x, title_y), title_font, text_color, border_width, border_color)
    add_text_border(draw, artist, (artist_x, artist_y), artist_font, text_color, border_width, border_color)


    dir, file_full_name = os.path.split(image_path)
    file_name, ext = os.path.splitext(file_full_name)
    info_image_file_path = f"{dir}/{file_name}_info{ext}"

    img.save(info_image_file_path)

    return info_image_file_path


if __name__ == '__main__':
    create_album_art(
        "dreamlike_diffusion\Thinking_Out_Loud_Ed_Sheeran.jpg", 
        "Thinking Out Loud", 
        "Ed Sheeran"
    )
