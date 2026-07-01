function parseIntField(obj: Record<string, string>, key: string): number {
    if (!obj.hasOwnProperty(key)) {
        throw new Error(`Key '${key}' not found in object.`);
    }

    const value = obj[key];
    const parsedInt = parseInt(value, 10);

    if (isNaN(parsedInt)) {
        throw new Error(`Value for key '${key}' is not a valid integer: ${value}`);
    }

    return parsedInt;
}

// Example usage:
const exampleObj = { age: '25', name: 'John' };
console.log(parseIntField(exampleObj, 'age')); // Output: 25
console.log(parseIntField(exampleObj, 'name')); // Error: Value for key 'name' is not a valid integer: John
