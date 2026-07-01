import { fetch } from 'node-fetch';

/**
 * Asynchronously fetches data from a specified URL and parses it as JSON.
 * 
 * @param url - The URL of the resource to fetch.
 * @returns A Promise that resolves with the parsed JSON object, or rejects with an error if the request fails.
 */
async function fetchJson(url: string): Promise<any> {
    try {
        const response = await fetch(url);
        // Check if the response is ok
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        // Parse the JSON response
        return response.json();
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}

// Example usage:
(async () => {
    try {
        const data = await fetchJson('https://api.example.com/data');
        console.log(data); // This will log the JSON object parsed from the URL
    } catch (error) {
        console.error(error);
    }
})();
