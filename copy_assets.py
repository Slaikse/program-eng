import os
import shutil

def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)
        else:
            copy_directory(s, d)

# Copy images
image_dirs = ['tiles', 'background', 'bombs', 'borders', 'deco']
for dir_name in image_dirs:
    src = os.path.join('..', 'assets', 'images', dir_name)
    dst = os.path.join('assets', 'images', dir_name)
    copy_directory(src, dst)

# Copy audio files
src_audio = os.path.join('..', 'assets', 'audio')
dst_audio = os.path.join('assets', 'audio')
copy_directory(src_audio, dst_audio)

print("Assets copied successfully!") 