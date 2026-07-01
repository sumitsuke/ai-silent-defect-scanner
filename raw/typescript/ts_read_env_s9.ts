/**
 * Reads an environment variable from the process.env object.
 * 
 * @param name - The name of the environment variable to read.
 * @returns The value of the specified environment variable or undefined if it does not exist.
 */
export function readEnv(name: string): string | undefined {
  return process.env[name];
}
