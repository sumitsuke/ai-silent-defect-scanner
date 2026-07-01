import * as fs from 'fs';

/**
 * Reads a JSON file and returns its content as an object.
 * 
 * @param path The path to the JSON file to be read.
 * @returns An object containing the data from the JSON file.
 */
function loadConfig(path: string): any {
    try {
        const rawData = fs.readFileSync(path, 'utf8');
        return JSON.parse(rawData);
    } catch (error) {
        console.error(`Error reading configuration file at ${path}:`, error);
        throw new Error('Failed to load configuration file');
    }
}

// Example usage:
(async () => {
    try {
        const config = await loadConfig('./config.json');
        console.log(config);
    } catch (error) {
        console.error(error.message);
    }
})();
