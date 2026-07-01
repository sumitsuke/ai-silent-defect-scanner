function readEnv(name: string): string | undefined {
  return process.env[name];
}

// Example usage:
const envValue = readEnv("MY_ENV_VAR");
if (envValue !== undefined) {
  console.log(`The value of MY_ENV_VAR is ${envValue}`);
} else {
  console.log(`Environment variable MY_ENV_VAR not found.`);
}
