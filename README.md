# Colorize Portraits

A Python project to colorize black and white portrait images using deep learning.

## Features
- Upload black & white portrait images
- Automatic colorization using a pretrained model
- Download the colorized result

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Dependencies
- streamlit
- opencv-python
- pillow
- numpy
- torch
- torchvision

## Notes
- For best results, use clear portrait images.
- The model used is based on OpenCV's DNN colorization or DeOldify (can switch later).


## links
 - https://github.com/AbhilipsaJena/Image_colorization-OpenCV/tree/main