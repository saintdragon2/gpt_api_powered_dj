from PIL import Image, ImageDraw, ImageFont

def create_album_art(image_path, title, artist):
    # 이미지 열기
    img = Image.open(image_path)

    # 이미지 크기 얻기
    width, height = img.size

    # 드로잉 객체 생성
    draw = ImageDraw.Draw(img)

    # 텍스트 크기 결정
    title_font_size = int(height * 0.07)
    artist_font_size = int(height * 0.05)

    # 폰트 설정
    title_font = ImageFont.truetype("malgun.ttf", title_font_size)
    artist_font = ImageFont.truetype("malgun.ttf", artist_font_size)
    # 맥
    # title_font = ImageFont.truetype("/Library/Fonts/Supplemental/AppleGothic.ttf", title_font_size)
    # artist_font = ImageFont.truetype("/Library/Fonts/Supplemental/AppleGothic.ttf", artist_font_size)

    # 텍스트 색상 설정 (흰색)
    text_color = (255, 255, 255)

    # 제목 위치 계산
    title_width, title_height = draw.textsize(title, font=title_font)
    title_x = (width - title_width) / 2
    title_y = (height - title_height) * 0.4

    # 아티스트명 위치 계산
    artist_width, artist_height = draw.textsize(artist, font=artist_font)
    artist_x = (width - artist_width) / 2
    artist_y = (height - artist_height) * 0.55

    # 텍스트 그리기
    draw.text((title_x, title_y), title, font=title_font, fill=text_color)
    draw.text((artist_x, artist_y), artist, font=artist_font, fill=text_color)

    # 결과 이미지 저장
    img.save(f"./dreamlike_diffusion/{title}_{artist}_album_art.jpg")

# 사용 예시
create_album_art(
    "dreamlike_diffusion/Uptown_Funk_Mark_Ronson_ft_Bruno_Mars.jpg", 
    "Laugh Now Cry Later ft. Lil Durk", 
    "Drake"
)
