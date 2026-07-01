import * as fs from 'fs';

/**
 * Loads configuration from a JSON file.
 *
 * @param path - The path to the JSON file.
 * @returns The parsed JSON object.
 */
function loadConfig(path: string): any {
  try {
    const configContent = fs.readFileSync(path, 'utf-8');
    return JSON.parse(configContent);
  } catch (error) {
    console.error(`Error loading configuration from ${path}:`, error);
    throw new Error('Failed to load configuration file.');
  }
}

// Example usage
const configPath = 'config.json';
try {
  const config = loadConfig(configPath);
  console.log('Configuration loaded:', config);
} catch (error) {
  console.error(error.message);
}
