// Function to read an item from localStorage and parse it as JSON
function getItem(key: string): any {
  try {
    // Retrieve the item from localStorage
    const item = localStorage.getItem(key);
    // Check if the item exists and is not null or undefined
    if (item !== null && item !== undefined) {
      // Parse the item as JSON
      return JSON.parse(item);
    }
    console.log("Item not found or invalid JSON in localStorage");
    return null;
  } catch (error) {
    console.error("Error parsing item from localStorage", error);
    return null;
  }
}

// Example usage:
const data = getItem("someKey");
console.log(data); // This will log the parsed JSON object from localStorage
