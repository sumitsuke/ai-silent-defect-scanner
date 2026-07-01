// Import necessary packages
import { env } from 'process';

/**
 * Reads an environment variable by name.
 * 
 * This function takes a single argument, `name`, which is a string representing the name of the environment variable to be read.
 * It returns the value of the environment variable as a string. If the environment variable does not exist or has no value, it throws an error.
 * 
 * @param {string} name - The name of the environment variable to read.
 * @returns {string} - The value of the environment variable.
 */
function readEnv(name: string): string {
    const value = env[name];
    if (value === undefined) {
        throw new Error(`Environment variable ${name} is not set.`);
    }
    return value;
}

// Example usage
try {
    console.log(readEnv('MY_ENV_VAR')); // Output: The value of MY_ENV_VAR
} catch (error) {
    console.error(error);
}
