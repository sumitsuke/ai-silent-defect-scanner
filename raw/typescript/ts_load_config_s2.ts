import fs from 'fs';
import path from 'path';

/**
 * Loads configuration data from a JSON file.
 * @param path The path to the JSON file.
 * @returns The parsed JSON object.
 */
function loadConfig(path: string): any {
  try {
    const configBuffer = fs.readFileSync(path, 'utf8');
    return JSON.parse(configBuffer);
  } catch (error) {
    console.error(`Error reading or parsing configuration from ${path}:`, error);
    throw new Error(`Failed to load configuration at ${path}`);
  }
}

// Example usage:
const configPath = 'config.json';
try {
  const config = loadConfig(configPath);
  console.log('Configuration loaded successfully:', config);
} catch (error) {
  // Handle the error, e.g., display a message or notify the user
}
