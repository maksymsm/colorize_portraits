import cv2
import numpy as np
import os

class ImageColorizer:
    def __init__(self):
        # Get the base directory (backend folder)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Define paths to model files
        self.prototxt_path = os.path.join(base_dir, 'colorization_deploy_v2.prototxt')
        self.caffemodel_path = os.path.join(base_dir, 'colorization_release_v2.caffemodel')
        self.points_path = os.path.join(base_dir, 'pts_in_hull.npy')
        
        # Load the model
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt_path, self.caffemodel_path)
        self.points = np.load(self.points_path)
        
        # Load model points
        self.points = self.points.transpose().reshape(2, 313, 1, 1)
        self.net.getLayer(self.net.getLayerId('class8_ab')).blobs = [self.points.astype('float32')]
        self.net.getLayer(self.net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, dtype='float32')]

    def colorize_image(self, image):
        # Convert to float32 and scale
        scaled = image.astype('float32') / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        # Run model
        self.net.setInput(cv2.dnn.blobFromImage(L))
        ab = self.net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

        # Combine with original L channel
        L_orig = cv2.split(lab)[0]
        colorized = np.concatenate((L_orig[:, :, np.newaxis], ab), axis=2)
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = np.clip(colorized, 0, 1)
        colorized = (255 * colorized).astype('uint8')

        return colorized 