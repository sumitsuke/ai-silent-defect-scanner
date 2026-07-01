/**
 * Reads a value from localStorage by key, parses it as JSON, and returns it.
 * 
 * @param {string} key - The key of the item to be retrieved.
 * @returns {any} The parsed value from localStorage or undefined if not found.
 */
function getItem(key: string): any {
    const storedValue = localStorage.getItem(key);
    return storedValue ? JSON.parse(storedValue) : undefined;
}

// Check function to verify the correctness of the solution
function check() {
    // Set a key-value pair in localStorage
    localStorage.setItem('exampleKey', '{"name": "John", "age": 30}');
    
    // Test the getItem function
    const retrievedItem = getItem('exampleKey');
    console.log(retrievedItem); // Expected output: { name: 'John', age: 30 }
    
    // Clean up by removing the key-value pair from localStorage
    localStorage.removeItem('exampleKey');
}

check();
