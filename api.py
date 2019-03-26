from flask import Flask, render_template, request, send_file
from io import BytesIO,StringIO
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import json, urllib.request
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      temp = BytesIO()
      modified = BytesIO()
      f = request.files['file']
      f.save(temp)
      #temp.seek(0)
      modified = make_meme("Si no esta en Javascript","esque no existe",temp)
      modified.seek(0)
      return send_file(modified,attachment_filename='test.jpeg', mimetype=f.mimetype)


def make_meme(topString, bottomString, temp):
   topString = request_to_andaluh(topString)
   bottomString = request_to_andaluh(bottomString)
   temp.seek(0)
   image_to_return = BytesIO()
   img = Image.open(temp)
   imageSize = img.size
   fontSize = int(imageSize[1]/5)
   font = ImageFont.truetype("fonts/RobotoCondensed-Bold.ttf", fontSize)
   topTextSize = font.getsize(topString)
   bottomTextSize = font.getsize(bottomString)
   while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
      fontSize = fontSize - 1
      font = ImageFont.truetype("fonts/RobotoCondensed-Bold.ttf", fontSize)
      topTextSize = font.getsize(topString)
      bottomTextSize = font.getsize(bottomString)

	# find top centered position for top text
   topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
   topTextPositionY = 0
   topTextPosition = (topTextPositionX, topTextPositionY)

   # find bottom centered position for bottom text
   bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
   bottomTextPositionY = imageSize[1] - bottomTextSize[1]
   bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

   draw = ImageDraw.Draw(img)

	# draw outlines
	# there may be a better way
   outlineRange = int(fontSize/15)
   for x in range(-outlineRange, outlineRange+1):
      for y in range(-outlineRange, outlineRange+1):
         draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
         draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

   draw.text(topTextPosition, topString, (255,255,255), font=font)
   draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

   img.save(image_to_return, format="jpeg")
   return image_to_return
	# img.save("temp.png")

def request_to_andaluh(string_to_andaluh):
   with urllib.request.urlopen("https://api.andaluh.es/epa?spanish="+string_to_andaluh) as url:
      translation = json.loads(url.read().decode())
      return translation["andaluh"]



if __name__ == '__main__':
    app.run( debug=True)