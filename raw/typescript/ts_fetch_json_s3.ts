import axios from 'axios';

/**
 * Asynchronously fetches data from a given URL and parses it as JSON.
 * 
 * @param url - The URL to which the data is fetched.
 * @returns A Promise that resolves to the parsed JSON object or rejects with an error.
 */
export async function fetchJson(url: string): Promise<any> {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error; // Re-throw the error to be handled by the caller
    }
}
