// Import the necessary package for environment variable handling
import { get } from 'dotenv';

/**
 * Reads an environment variable from the process.env object.
 * 
 * @param name - The name of the environment variable to read.
 * @returns The value of the specified environment variable, or undefined if not found.
 */
function readEnv(name: string): string | undefined {
    // Use the get function from dotenv to retrieve the environment variable
    const envValue = get(name);
    
    // Return the retrieved environment variable value, or undefined if it does not exist
    return envValue;
}

// Example usage:
const dbHost = readEnv('DB_HOST');
console.log(dbHost); // Output: The value of DB_HOST from process.env

const username = readEnv('USERNAME');
console.log(username); // Output: The value of USERNAME from process.env
