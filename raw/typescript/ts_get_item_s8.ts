function getItem(key: string): any {
  const item = localStorage.getItem(key);
  if (item !== null) {
    try {
      return JSON.parse(item);
    } catch (error) {
      console.error(`Failed to parse JSON from localStorage: ${key}`, error);
      return null;
    }
  }
  return null;
}

// Example usage:
const myItem = getItem('myKey');
console.log(myItem); // Output: { someProperty: 'someValue' }
