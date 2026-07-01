function parseIntField(obj: Record<string, string>, key: string): number {
  // Check if the key exists in the object and its value can be parsed to an integer
  if (key in obj && isNaN(parseInt(obj[key]))) {
    throw new Error(`The value of key "${key}" cannot be converted to an integer.`);
  }

  return parseInt(obj[key]);
}

// Example usage:
const exampleObj = { age: "30", name: "John" };
console.log(parseIntField(exampleObj, "age")); // Output: 30
console.log(parseIntField(exampleObj, "name")); // Throws an error: The value of key "name" cannot be converted to an integer.
