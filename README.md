# face-filter
Face filter using python

[Assignment/Purpose]
Create program that adds a facial filter utilizing OpenCV

[Name(s)]
Ronny Oropeza

[Resources]
Intro Material/References-
https://analyticsindiamag.com/how-to-build-your-own-face-filter-with-opencv/
https://pysource.com/2019/03/25/pigs-nose-instagram-face-filter-opencv-with-python/

[Notes]
Install Guide-
1. Install Visual Studio with Desktop Development with C++ (ensure cmake tools for windows is checked)
    https://visualstudio.microsoft.com/
2. Install required packages with pip (commands below)
    *may require administrative privileges
    pip install cmake
    pip install dlib
    pip install opencv-python
    pip install imutils
3. Download 'shape_predictor.dat' (and optional pngs and test video) and place within same directory
   link: https://www.dropbox.com/sh/ngk5k7lxl976plr/AADSakT3wzO0n_zhOtwcZ7kda?dl=0

[TODO]
- Improve developer readability
- Face Filter Options - Full Face, mouth, eyes, forehead, background
- Face Filter Types - Static, Dynamic
- Add function to insert video/photo to apply filter to
- Improve stability

[Known Issues]
- Crashes when multiple faces are introduced to frame
