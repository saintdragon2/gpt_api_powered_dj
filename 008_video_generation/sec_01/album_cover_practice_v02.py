from PIL import Image, ImageDraw, ImageFont
import os

def add_info_to_file_path(file_path, info_string):
    # 파일의 기본 이름과 확장자 분리
    base_name, file_extension = os.path.splitext(file_path)

    # 새로운 파일 경로 생성
    new_file_path = f"{base_name}{info_string}{file_extension}"

    return new_file_path

def add_text_border(draw, text, position, font, fill, border_width, border_color):
    x, y = position
    for x_offset in range(-border_width, border_width + 1):
        for y_offset in range(-border_width, border_width + 1):
            draw.text((x + x_offset, y + y_offset), text, font=font, fill=border_color)
    
    draw.text((x, y), text, font=font, fill=fill)

def create_album_art(image_path, title, artist, output_path='__info'):
    # 이미지 열기
    album_art = Image.open(image_path)

    # 이미지 크기 얻기
    width, height = album_art.size

    # 폰트 및 크기 설정
    font_size_title = int(min(width, height) * 0.08)
    font_size_artist = int(min(width, height) * 0.05)

    # Windows
    title_font = ImageFont.truetype("malgun.ttf", font_size_title)
    artist_font = ImageFont.truetype("malgun.ttf", font_size_artist)

    # Mac
    # title_font = ImageFont.truetype("/Library/Fonts/Supplemetal/AppleGothic.ttf", font_size_title)
    # artist_font = ImageFont.truetype("/Library/Fonts/Supplemetal/AppleGothic.ttf", font_size_artist)

    # 이미지에 텍스트 추가
    draw = ImageDraw.Draw(album_art)

    
    # 제목 및 아티스트 텍스트의 검은색 테두리를 추가
    outline_color = (0, 0, 0)  # 검은색

    # 텍스트의 위치 조정
    outline_width = int(width * 0.01)  # 테두리 두께 조정

    # 텍스트가 이미지 폭을 초과하지 않도록 조정
    max_text_width = width * 0.9  # 이미지 폭의 90%
    
    while title_font.getlength(title) > max_text_width:
        font_size_title -= 1
        title_font = ImageFont.truetype("malgun.ttf", font_size_title)
        
    while artist_font.getlength(artist) > max_text_width:
        font_size_artist -= 1
        artist_font = ImageFont.truetype("malgun.ttf", font_size_artist)

    # 제목 위치 및 색상 설정
    title_width = title_font.getlength(title)
    title_x = width * 0.5 - title_width * 0.5
    title_y = height * 0.7
    title_color = (255, 255, 255)  # 흰색

    # 아티스트 위치 및 색상 설정
    artist_width = artist_font.getlength(artist)
    artist_x = width * 0.5 - artist_width * 0.5
    artist_y = title_y + font_size_title + height * 0.015
    artist_color = (255, 255, 255)  # 흰색

    # 제목 텍스트와 테두리 추가
    add_text_border(draw, title, (title_x, title_y), title_font, title_color, outline_width, outline_color)

    # 아티스트 텍스트와 테두리 추가
    add_text_border(draw, artist, (artist_x, artist_y), artist_font, artist_color, outline_width, outline_color)

    output_path = add_info_to_file_path(image_path, '__info')

    # 결과 이미지 저장
    album_art.save(output_path)


if __name__ == '__main__':
    create_album_art(
        "./dreamlike_diffusion/Uptown_Funk_Mark_Ronson_ft._Bruno_Mars.jpg", 
        "Uptown Funk", 
        "Mark Ronson ft. Bruno Mars", 
    )

    # create_album_art(
    #     "dreamlike_diffusion\Boy_With_Luv_방탄소년단_ft._Halsey.jpg",
    #     "Boy With Luv",
    #     "방탄소년단 ft. Halsey"
    # )
    
    # create_album_art(
    #     "C:\github\gpt_api_powered_dj\dreamlike_diffusion\내_마음에_주단을_깔고_신해철.jpg",
    #     "내 마음에 주단을 깔고 (KBS 열림음악회 버전)",
    #     "산울림, YB, 시나위, BTS, 르세라핌, 노사연, 김종서"
    # )