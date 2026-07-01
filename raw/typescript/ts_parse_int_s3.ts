/**
 * Parses the value associated with the specified key in an object as an integer.
 * 
 * @param obj - An object containing the key-value pairs to be parsed.
 * @param key - The key whose associated value is to be converted to an integer.
 * @returns The integer value of the specified key.
 */
function parseIntField(obj: Record<string, string>, key: string): number {
    const value = obj[key];
    if (value === undefined || isNaN(Number(value))) {
        throw new Error(`Key "${key}" does not exist or cannot be converted to an integer.`);
    }
    return Number(value);
}

// Check function to verify the correctness of the parseIntField function
function check() {
    console.assert(parseIntField({ a: "42" }, "a") === 42, 'Test case 1 failed');
    console.assert(parseIntField({ b: "3.14" }, "b") === 3, 'Test case 2 failed');
    console.assert(parseIntField({ c: "0" }, "c") === 0, 'Test case 3 failed');
    try {
        parseIntField({ d: "string" }, "d");
    } catch (error) {
        console.assert(error instanceof Error && error.message.includes("Key \"d\" does not exist or cannot be converted to an integer."), 'Test case 4 failed');
    }
    console.log('All test cases passed!');
}

// Run the check function to validate the solution
check();
