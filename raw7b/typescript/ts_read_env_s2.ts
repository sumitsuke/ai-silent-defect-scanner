function readEnv(name: string): string | undefined {
    return process.env[name];
}

// Example usage:
const dbHost = readEnv('DB_HOST');
if (dbHost) {
    console.log(`Database host is: ${dbHost}`);
} else {
    console.log('Environment variable DB_HOST is not set.');
}
