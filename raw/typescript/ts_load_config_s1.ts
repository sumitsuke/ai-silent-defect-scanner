import * as fs from 'fs';

function loadConfig(path: string): any {
    try {
        // Read the JSON file synchronously
        const configData = fs.readFileSync(path, 'utf8');
        
        // Parse the JSON data into an object
        const configObject = JSON.parse(configData);
        
        return configObject;
    } catch (error) {
        console.error(`Error loading configuration from ${path}:`, error);
        throw error; // Re-throw the error to propagate it up the call stack
    }
}

// Example usage:
try {
    const config = loadConfig('./config.json');
    console.log(config); // Output: The parsed JSON object from config.json
} catch (error) {
    console.error(error);
}
