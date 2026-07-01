// Function to read an environment variable
function readEnv(name: string): string | undefined {
    // Retrieve the environment variable using process.env
    const envValue = process.env[name];
    return envValue;
}

// Example usage:
const myVariable = readEnv('MY_VARIABLE');
console.log(myVariable); // Output: "my_value"
