function parseIntField(obj: Record<string, string>, key: string): number {
  // Check if the key exists in the object
  if (obj.hasOwnProperty(key)) {
    // Attempt to parse the value of the key as an integer
    const value = parseInt(obj[key], 10);
    // Return the parsed integer
    return value;
  } else {
    // If the key does not exist, throw an error or handle it as needed
    throw new Error(`Key "${key}" does not exist in the object.`);
  }
}

// Example usage:
const exampleObject = { id: "12345", name: "John Doe" };
try {
  const intValue = parseIntField(exampleObject, "id");
  console.log(intValue); // Output: 12345
} catch (error) {
  console.error(error.message);
}
