# Colorize Portraits

A web application to colorize black and white portrait images using deep learning. The app consists of a React frontend and a Flask backend powered by OpenCV's DNN colorization model.

## Features
- Upload black & white portrait images via the web UI
- Automatic colorization using a pretrained deep learning model
- Download the colorized result

## Project Structure
```
colorize_portraits/
├── backend/       # Flask API for colorization
│   ├── app.py
│   ├── colorization_deploy_v2.prototxt
│   ├── colorization_release_v2.caffemodel
│   └── pts_in_hull.npy
├── frontend/      # React app for user interface
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── README.md
└── ...
```

## Backend Setup (Flask)
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask API:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5050`.

## Frontend Setup (React)
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React app:
   ```bash
   npm start
   ```
   The app will be available at `http://localhost:3000` by default.

## Usage
- Open the frontend in your browser.
- Upload a black & white portrait image.
- The image will be sent to the backend for colorization.
- View and download the colorized result.

## Backend Dependencies
- Flask
- flask-cors
- numpy
- opencv-python
- pillow

## Frontend Dependencies
- React
- axios

## Notes
- For best results, use clear portrait images.
- The backend uses OpenCV's DNN colorization model.

## References
- https://github.com/AbhilipsaJena/Image_colorization-OpenCV/tree/main