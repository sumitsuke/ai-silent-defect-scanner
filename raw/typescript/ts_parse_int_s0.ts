/**
 * Converts the value associated with the specified key in an object to an integer.
 * If the conversion is not possible or the value is not a number, it returns null.
 * 
 * @param obj - The object containing the key-value pairs.
 * @param key - The key whose value will be converted to an integer.
 * @returns The integer value of the specified key in the object, or null if the conversion fails.
 */
function parseIntField(obj: Record<string, string>, key: string): number | null {
    const value = obj[key];
    if (typeof value === 'string' && !isNaN(Number(value))) {
        return parseInt(value);
    }
    return null;
}

// Check function to verify the correctness of the generated function
function check() {
    console.log(parseIntField({ foo: "42" }, "foo")); // Expected output: 42
    console.log(parseIntField({ bar: "not-a-number" }, "bar")); // Expected output: null
    console.log(parseIntField({ baz: "" }, "baz")); // Expected output: null
    console.log(parseIntField({ qux: "12345678901234567890" }, "qux")); // Expected output: 12345678901234567890
}

// Run the check function to perform tests
check();
