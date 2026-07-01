import axios from 'axios';

export async function fetchJson(url: string): Promise<any> {
  try {
    // Make the HTTP GET request to the specified URL
    const response = await axios.get(url);

    // Check if the response status is OK (200)
    if (response.status === 200) {
      // Parse the JSON body from the response
      return response.data;
    } else {
      throw new Error(`Failed to fetch data. Status code: ${response.status}`);
    }
  } catch (error) {
    // Handle any errors that occur during the request or parsing
    console.error('An error occurred while fetching the JSON:', error);
    throw error;
  }
}

// Example usage:
(async () => {
  try {
    const data = await fetchJson('https://api.example.com/data');
    console.log(data);
  } catch (error) {
    console.error(error);
  }
})();
