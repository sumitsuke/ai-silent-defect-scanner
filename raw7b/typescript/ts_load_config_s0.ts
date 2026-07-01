import * as fs from 'fs';

/**
 * Loads a configuration file from the given path.
 * @param {string} path - The path to the JSON file.
 * @returns {Promise<any>} A promise that resolves with the parsed JSON object.
 */
export function loadConfig(path: string): Promise<any> {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) {
        reject(err);
      } else {
        try {
          const config = JSON.parse(data);
          resolve(config);
        } catch (parseErr) {
          reject(parseErr);
        }
      }
    });
  });
}
