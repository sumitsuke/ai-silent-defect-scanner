import axios from 'axios';

/**
 * Fetches JSON data from a given URL.
 * 
 * @param url - The URL to fetch.
 * @returns A Promise that resolves with the parsed JSON data or rejects with an error.
 */
export async function fetchJson(url: string): Promise<any> {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error('Error fetching JSON:', error);
        throw error;
    }
}
