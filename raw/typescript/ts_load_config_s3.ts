import { readFile } from 'fs';

/**
 * Reads a JSON file and returns its content as an object.
 * 
 * @param path - The path to the JSON file to read.
 * @returns The parsed JSON object.
 */
function loadConfig(path: string): any {
    return readFile(path, 'utf8', (err, data) => {
        if (err) {
            throw new Error(`Error reading file ${path}: ${err.message}`);
        }
        try {
            return JSON.parse(data);
        } catch (parseErr) {
            throw new Error(`Error parsing JSON in file ${path}: ${parseErr.message}`);
        }
    });
}

// Example usage
try {
    const config = loadConfig('config.json');
    console.log(config); // Output the parsed JSON object
} catch (error) {
    console.error(error);
}
