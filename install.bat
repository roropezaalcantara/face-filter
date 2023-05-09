echo Ensure to install 'Visual Studio' with 'Desktop Development with C++' (ensure cmake tools for windows is checked)
echo https://visualstudio.microsoft.com/
echo
echo Press any key to Continue...
pause > nul
pip install cmake
pip install dlib
pip install opencv-python
pip install imutils
@echo off
echo.
echo Install Complete
echo Press any key to Continue...
pause > nul