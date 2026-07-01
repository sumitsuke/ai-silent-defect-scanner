import * as fs from 'fs';
import { parse } from 'json5';

/**
 * Loads a JSON configuration file and parses it into an object.
 * 
 * @param path The path to the JSON file.
 * @returns An object representing the parsed configuration.
 */
function loadConfig(path: string): any {
    try {
        const jsonData = fs.readFileSync(path, 'utf-8');
        return parse(jsonData);
    } catch (error) {
        console.error(`Failed to load config from ${path}:`, error);
        throw error;
    }
}

// Example usage:
loadConfig('config.json')
    .then(config => {
        console.log(config); // Output the parsed configuration object
    })
    .catch(error => {
        console.error('Error loading or parsing config:', error);
    });
