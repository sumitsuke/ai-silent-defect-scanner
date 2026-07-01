function parseIntField(obj: Record<string, string>, key: string): number {
  // Check if the value exists in the object and is not null or undefined
  if (obj.hasOwnProperty(key) && obj[key] !== null && obj[key] !== undefined) {
    const value = obj[key];
    // Attempt to parse the value as an integer using parseInt
    const parsedValue = parseInt(value, 10);
    return parsedValue;
  } else {
    // Return NaN if parsing fails or key does not exist
    return NaN;
  }
}

// Example usage:
const obj = { id: "123", name: "John" };
const key = "id";
console.log(parseIntField(obj, key)); // Output: 123

const invalidObj = { id: null, name: "Jane" };
const invalidKey = "name";
console.log(parseIntField(invalidObj, invalidKey)); // Output: NaN
