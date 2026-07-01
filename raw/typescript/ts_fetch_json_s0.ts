import { existsSync } from 'fs';
import { readFileSync } from 'fs';

async function fetchJson(url: string): Promise<any> {
    try {
        // Check if the file already exists to avoid multiple fetches
        const filePath = `./cache/${url.replace('https://', '')}.json`;
        if (existsSync(filePath)) {
            console.log(`Fetching from cache for ${url}`);
            return JSON.parse(readFileSync(filePath));
        } else {
            console.log(`Fetching from server for ${url}`);
            // Fetch the JSON body from the URL
            const response = await fetch(url);
            const data = await response.json();
            // Save the fetched data to a file in the cache directory
            fs.writeFileSync(filePath, JSON.stringify(data), { encoding: 'utf-8' });
            return data;
        }
    } catch (error) {
        console.error(`Error fetching ${url}:`, error);
        throw error;
    }
}

// Example usage
fetchJson('https://api.example.com/data')
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Failed to fetch data:', error);
    });
