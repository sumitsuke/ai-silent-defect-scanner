import * as fs from 'fs';

function loadConfig(path: string): any {
  try {
    const data = fs.readFileSync(path, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`Failed to read or parse config file at ${path}:`, error);
    throw error;
  }
}
