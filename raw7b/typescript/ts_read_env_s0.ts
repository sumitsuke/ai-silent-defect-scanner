function readEnv(name: string): string | undefined {
    return process.env[name];
}

// Example usage:
const myEnvironmentVariable = readEnv('MY_ENV_VARIABLE');
console.log(myEnvironmentVariable);
