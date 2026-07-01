function getItem(key: string): any {
  // Retrieve the item from localStorage using the provided key
  const item = localStorage.getItem(key);
  
  // Check if the item exists in localStorage
  if (item !== null) {
    try {
      // Attempt to parse the JSON string into a JavaScript object
      return JSON.parse(item);
    } catch (error) {
      console.error(`Error parsing JSON for key ${key}:`, error);
      // Return null or handle the error as needed
      return null;
    }
  } else {
    // If the item does not exist, return undefined
    return undefined;
  }
}

// Example usage:
console.log(getItem('myKey')); // This will print whatever is stored in localStorage under key 'myKey'
