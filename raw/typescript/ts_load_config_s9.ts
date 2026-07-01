import * as fs from 'fs';

/**
 * Loads the configuration from a JSON file.
 * @param path - The path to the JSON file.
 * @returns An object representing the loaded configuration.
 */
function loadConfig(path: string): any {
    try {
        const configData = fs.readFileSync(path, 'utf8');
        return JSON.parse(configData);
    } catch (error) {
        throw new Error(`Error loading configuration from ${path}: ${error.message}`);
    }
}

// Example usage:
try {
    const config = loadConfig('config.json');
    console.log(config);
} catch (err) {
    console.error(err.message);
}
