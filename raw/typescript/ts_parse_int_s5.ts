/**
 * Parses and returns an integer from a JSON-like object using a specified key.
 * 
 * @param obj - An object containing key-value pairs representing data in a JSON-like structure.
 * @param key - The key in the object whose associated value is to be parsed as an integer.
 * @returns The integer value of the specified key if it exists and can be parsed, otherwise undefined.
 */
function parseIntField(obj: Record<string, string>, key: string): number | undefined {
    const value = obj[key];
    // Check if the value is a valid number before attempting to parse
    if (typeof value === 'string' && /^\d+$/.test(value)) {
        return parseInt(value);
    }
    return undefined;
}

// Function to check the correctness of the parseIntField function
function check() {
    console.assert(parseIntField({ age: "25" }, "age") === 25, 'Test with valid integer');
    console.assert(parseIntField({ score: "88.9" }, "score") === undefined, 'Test with non-integer string value');
    console.assert(parseIntField({ isActive: "true" }, "isActive") === undefined, 'Test with boolean value');
    console.assert(parseIntField({ amount: "100.50" }, "amount") === 100, 'Test with decimal string value');
}

// Run the check function to verify the correctness of the parseIntField function
check();
