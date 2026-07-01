import * as fs from 'fs';

/**
 * Reads a JSON file and returns its content as an object.
 * @param path The path to the JSON file.
 * @returns A Promise resolving to the parsed JSON object.
 */
async function loadConfig(path: string): Promise<any> {
    try {
        const data = await fs.promises.readFile(path, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error(`Error reading or parsing the file at ${path}:`, error);
        throw error; // Re-throw the error to be handled by the caller
    }
}

// Example usage:
(async () => {
    try {
        const config = await loadConfig('./config.json');
        console.log(config); // Output: The parsed JSON object
    } catch (error) {
        // Handle any errors that occurred during file loading or parsing
    }
})();
