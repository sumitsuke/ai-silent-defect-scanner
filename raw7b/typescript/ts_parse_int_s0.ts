function parseIntField(obj: Record<string, string>, key: string): number | undefined {
    // Check if the key exists in the object
    if (key in obj) {
        const value = obj[key];
        // Attempt to parse the value as an integer
        const parsedValue = parseInt(value, 10);
        // Return the parsed value if it's not NaN (Not-a-Number)
        return isNaN(parsedValue) ? undefined : parsedValue;
    }
    // Return undefined if the key does not exist in the object
    return undefined;
}

// Example usage:
const exampleObj = {
    age: "25",
    height: "180cm",
    weight: "75kg"
};

console.log(parseIntField(exampleObj, "age")); // Output: 25
console.log(parseIntField(exampleObj, "height")); // Output: undefined (cannot be parsed as an integer)
console.log(parseIntField(exampleObj, "weight")); // Output: undefined (cannot be parsed as an integer)
console.log(parseIntField(exampleObj, "gender")); // Output: undefined (key does not exist)
