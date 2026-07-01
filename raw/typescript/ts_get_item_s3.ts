/**
 * Retrieves an item from localStorage based on the provided key.
 * Parses the retrieved data as JSON before returning it.
 * 
 * @param key The key of the item to retrieve.
 * @returns The parsed JSON value associated with the given key.
 */
function getItem(key: string): any {
    const storedValue = localStorage.getItem(key);
    if (storedValue) {
        try {
            return JSON.parse(storedValue);
        } catch (error) {
            console.error('Error parsing JSON:', error);
            // Handle the error, e.g., log it or return a default value
            return null;
        }
    }
    return null; // Return null if no item is found or parsing fails
}

// Example usage:
const myItem = getItem("myData");
console.log(myItem); // Output will be the parsed JSON object from localStorage
