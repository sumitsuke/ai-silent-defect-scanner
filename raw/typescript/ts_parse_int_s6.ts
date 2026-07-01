function parseIntField(obj: Record<string, string>, key: string): number {
    const value = obj[key];
    if (typeof value !== 'string' || !value.trim()) {
        throw new Error(`Key '${key}' does not exist or is empty.`);
    }

    const parsedValue = parseInt(value, 10);
    if (isNaN(parsedValue)) {
        throw new Error(`The value associated with key '${key}' cannot be converted to an integer.`);
    }

    return parsedValue;
}

// Example usage:
const obj = { id: '123', name: 'Alice' };
console.log(parseIntField(obj, 'id')); // Output: 123
