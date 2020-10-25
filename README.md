# Image-to-Pdf
Images to pdf for assignment submission \
To execute: run.py \
*Note:* While selecting multiple file choosing one at a time is suggested.

## Requirements
* Python
* Pillow -> `pip install pillow` 
Or,
* `pip install -r requirements.txt` 
* *Note:* Update Pip 
* `python -m pip install --upgrade pip`

## Information
After running the program, pdf folder is made on which pdf files are saved in number i.e. 1.pdf, 2.pdf, 3.pdf, etc.

## For the case of Linux
Tkinter might not be installed by default so we have to install it manually.

### For Debian/Ubuntu:

#### Python 2

sudo apt-get install python-tk

sudo apt-get install python-imaging python-pil.imagetk

#### Python 3

sudo apt-get install python3-tk

sudo apt-get install python3-pil python3-pil.imagetk
### For Archlinux:

sudo pacman -S python-pillow  

It will install the package and you can use it: from PIL import ImageTk
