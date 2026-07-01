function getItem(key: string): any {
    const item = localStorage.getItem(key);
    if (item !== null) {
        try {
            return JSON.parse(item);
        } catch (error) {
            console.error(`Error parsing JSON from localStorage for key ${key}:`, error);
            return null; // Return null or handle the error as needed
        }
    }
    return null;
}

// Example usage:
const myItem = getItem('myKey');
console.log(myItem); // Output: { /* parsed JSON object */ }
