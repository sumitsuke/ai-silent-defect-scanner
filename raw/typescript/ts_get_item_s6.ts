function getItem(key: string): any {
  // Get the item from localStorage
  const item = localStorage.getItem(key);

  // Check if the item exists in localStorage
  if (item !== null) {
    try {
      // Parse the item as JSON
      return JSON.parse(item);
    } catch (error) {
      console.error('Error parsing JSON:', error);
      return null;
    }
  } else {
    console.log(`Item with key ${key} does not exist.`);
    return null;
  }
}

// Example usage:
const data = getItem('userSettings');
if (data) {
  console.log(data); // Output: { username: 'JohnDoe', theme: 'dark' }
}
