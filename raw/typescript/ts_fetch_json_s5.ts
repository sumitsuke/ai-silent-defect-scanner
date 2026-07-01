import axios from 'axios';

export const fetchJson = async (url: string): Promise<any> => {
  try {
    const response = await axios.get(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the JSON:', error);
    throw error; // Rethrow the error for further handling
  }
};
