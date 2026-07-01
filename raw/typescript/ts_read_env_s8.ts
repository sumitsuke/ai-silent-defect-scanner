function readEnv(name: string): string | undefined {
  return process.env[name];
}

// Example usage:
const apiKey = readEnv("API_KEY");
console.log(apiKey); // Output will be the value of API_KEY from the environment, or undefined if it's not set.
