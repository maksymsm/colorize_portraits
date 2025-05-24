import axios from 'axios';

const API_URL = 'http://localhost:5050';

export const colorizeImage = async (coloredImage, grayscaleImage) => {
  const formData = new FormData();
  formData.append('colored_image', coloredImage);
  formData.append('grayscale_image', grayscaleImage);
  
  try {
    const response = await axios.post(`${API_URL}/colorize`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });
    
    if (response.data?.colorized_image?.length > 0 && response.data?.metrics) {
      return {
        colorizedImageUrl: `data:image/png;base64,${response.data.colorized_image}`,
        metrics: response.data.metrics
      };
    }
    
    throw new Error('Invalid response format - missing or invalid image data');
  } catch (error) {
    throw new Error('Failed to process images. ' + (error.response?.data?.error || error.message || ''));
  }
}; 