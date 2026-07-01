function getItem(key: string): any {
    // Retrieve the item from localStorage
    const item = localStorage.getItem(key);

    // Check if the item exists and is not null
    if (item !== null) {
        try {
            // Parse the JSON string to an object
            return JSON.parse(item);
        } catch (error) {
            console.error('Error parsing JSON:', error);
            return undefined;
        }
    }

    // If the item does not exist or is null, return undefined
    return undefined;
}
