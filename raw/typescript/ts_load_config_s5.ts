import { readFile } from 'fs/promises';

/**
 * Reads a JSON file at the given path and returns its contents as an object.
 * 
 * @param path - The path to the JSON file.
 * @returns A promise that resolves to the parsed JSON object.
 */
export async function loadConfig(path: string): Promise<any> {
    const content = await readFile(path, 'utf8');
    return JSON.parse(content);
}

// Example usage:
(async () => {
    try {
        const config = await loadConfig('config.json');
        console.log(config); // This will log the parsed JSON object
    } catch (error) {
        console.error('Error loading configuration:', error);
    }
})();
