// Define the readEnv function to retrieve an environment variable
function readEnv(name: string): string | undefined {
  // Access the environment variable by its name
  return process.env[name];
}

// Example usage:
const myVariable = readEnv('MY_VARIABLE');
console.log(myVariable); // Output: The value of MY_VARIABLE from the environment

// Check function to verify the correctness of the readEnv function
function checkReadEnv() {
  console.assert(readEnv('NODE_ENV') === process.env.NODE_ENV, 'Node_ENV should be retrieved correctly');
  console.assert(readEnv('MY_VARIABLE') !== undefined && readEnv('MY_VARIABLE') === 'Hello', 'MY_VARIABLE should be retrieved with a specific value');
}

// Run the check function to test the readEnv function
checkReadEnv();
