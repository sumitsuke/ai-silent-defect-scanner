/**
 * Retrieves the integer value associated with the specified key in an object.
 * If the value is not a valid integer, it throws a TypeError.
 *
 * @param obj - The object containing the key-value pairs.
 * @param key - The key whose associated value should be retrieved.
 * @returns The integer value corresponding to the key.
 */
function parseIntField(obj: Record<string, string>, key: string): number {
    const value = obj[key];
    if (!Number.isInteger(Number(value))) {
        throw new TypeError(`The value for key "${key}" is not a valid integer.`);
    }
    return Number(value);
}

// Example usage:
const data = { score: '123' };
try {
    const result = parseIntField(data, 'score');
    console.log(result); // Output: 123
} catch (error) {
    console.error(error.message); // Expected output: The value for key "score" is not a valid integer.
}
