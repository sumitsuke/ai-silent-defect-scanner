function getItem(key: string): any {
  // Retrieve the value from localStorage
  const item = localStorage.getItem(key);
  
  // If the item exists, parse it as JSON
  if (item) {
    try {
      return JSON.parse(item);
    } catch (error) {
      console.error(`Error parsing JSON for key ${key}:`, error);
      return null;
    }
  }
  
  // Return null or a default value if no item is found
  return null; // You can change this to a specific default value based on your needs
}
