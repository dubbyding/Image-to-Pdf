import os
from PIL import Image

dir_path = os.path.dirname(os.path.realpath(__file__))

initial = 0
image_list = []

# Checking if pdf folder exists and checks to name the file
if not os.path.isdir(dir_path+'/pdf'):
    os.makedirs(dir_path+'/pdf')
else:
    name = list(os.listdir(dir_path+'/pdf'))
    if name == []:
        name = '1'
    else:
        name = str(int(name[-1].split('.')[0: -1][0]) + 1)

for entry in os.scandir(dir_path+'/Images'):
    if entry.is_dir():
        continue
    ext = entry.name.split('.')[-1]
    if ext == 'py' or ext == 'md':
        continue
    if initial == 0:
        im1 = Image.open(dir_path+'/Images/'+entry.name, mode='r').convert('RGB')
        initial = initial + 1
    else:
        image_list.append(Image.open(dir_path+'/Images/'+entry.name, mode='r').convert('RGB'))
    os.remove(dir_path+'/Images/'+entry.name)
try:
    if image_list == []:
        im1.save(dir_path+'/pdf/'+name+'.pdf', mode='r')
    else:
        im1.save(dir_path+'/pdf/'+name+'.pdf', mode='r',save_all = True, append_images = image_list)
except:
    pass
