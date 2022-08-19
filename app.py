import requests
from bs4 import BeautifulSoup
from flask import Flask, send_file
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def get_meme():
    url = 'https://www.commitstrip.com/?random=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find_all('div', class_='entry-content')
    img = div[0].find('img')['src']
    return img

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def return_meme():
    img_url = get_meme()
    res = requests.get(img_url, stream=True)
    res.raw.decode_content = True
    img = Image.open(res.raw)
    return serve_pil_image(img)

if __name__ == "__main__":
    app.run(host='0.0.0.0')