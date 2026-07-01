import * as fs from 'fs';

/**
 * Loads a JSON configuration file at the specified path.
 * 
 * @param path - The path to the JSON file.
 * @returns The parsed JSON object.
 */
function loadConfig(path: string): any {
    try {
        const data = fs.readFileSync(path, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Error reading or parsing JSON:', error);
        throw new Error(`Failed to load configuration file at ${path}`);
    }
}

// Example usage
const configPath = './config.json';
try {
    const config = loadConfig(configPath);
    console.log('Configuration loaded:', config);
} catch (error) {
    console.error('Error loading configuration:', error);
}
