/**
 * Retrieves the value associated with the given key in localStorage, parses it as JSON, and returns it.
 * 
 * @param key The key of the item to retrieve from localStorage.
 * @returns The parsed value retrieved from localStorage.
 */
function getItem(key: string): any {
    try {
        const value = localStorage.getItem(key);
        if (value) {
            return JSON.parse(value);
        }
    } catch (error) {
        console.error('Error parsing JSON from localStorage:', error);
    }
    return null;
}

// Example usage:
const item = getItem('myItem');
console.log(item); // Output will be the parsed value of 'myItem' stored in localStorage, or null if not found.
