import axios from 'axios';

async function fetchJson(url: string): Promise<any> {
  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching JSON:', error);
    throw error;
  }
}

// Example usage:
fetchJson('https://api.example.com/data')
  .then(data => console.log(data))
  .catch(error => console.error('Failed to fetch data:', error));
