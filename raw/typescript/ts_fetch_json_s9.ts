import axios from 'axios';

/**
 * Asynchronously fetches a JSON response from the specified URL.
 * 
 * @param url The URL of the JSON resource to fetch.
 * @returns A promise that resolves with the parsed JSON data or rejects with an error.
 */
export async function fetchJson(url: string): Promise<any> {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error(`Failed to fetch JSON from ${url}:`, error);
        throw error; // Re-throw the error to propagate it up the call stack
    }
}

// Example usage:
async function main() {
    try {
        const jsonData = await fetchJson('https://api.example.com/data');
        console.log(jsonData); // Output: JSON data parsed from the response
    } catch (error) {
        console.error(error);
    }
}
