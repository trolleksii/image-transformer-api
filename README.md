# Image Transformer
Simple app that takes an image from post request and transform it according to the parameters passed in URL.

## How to use it
1. Navigate to the interesting endpoint
2. Attach an image file and upload it
3. You will receive modified image in response

## Some use examples:

`/api/rotate/cw/90/` - rotate image by 90° clockwise
`/api/rotate/ccw/43/` - rotate image by 43° counterclockwise
`/api/resize/90/` - resize image to 90% of its original size
`/api/bw/` - convert colourspace from RGB to black and white


## Installation instructions
1. Install Python3, pip, venv:<br>
`sudo apt install python3 python3-pip python3-venv`
2. Clone this repository:<br>
```
mkdir project
cd ./project
git clone https://github.com/trolleksii/image_transformer.git
```
3. Create a new virtual environment with Python 3 interpreter:<br>
 `virtualenv -p python3 ./venv`
4. Activate it:<br>
 `source ./venv/bin/activate`
5. Install required packages from requirements.txt:<br>
 `pip install -r ./image-transformer/requirements.txt`
6. `cd` into ./image-transformer:<br>
 `cd ./image-transformer/`
7. Run tests to make sure that everything is working as it should:<br>
 `python manage.py test`
