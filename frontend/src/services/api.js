import axios from 'axios';

const API_URL = 'http://localhost:5050';

export const colorizeImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  
  try {
    const response = await axios.post(`${API_URL}/colorize`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    if (response.data && response.data.image) {
      return {
        imageUrl: `data:image/png;base64,${response.data.image}`,
        metrics: response.data.metrics
      };
    }
    
    throw new Error('Invalid response format - missing image data');
  } catch (error) {
    throw new Error('Failed to colorize image. ' + (error.response?.data?.error || error.message || ''));
  }
}; 