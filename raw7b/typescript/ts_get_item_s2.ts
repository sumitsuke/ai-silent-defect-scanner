function getItem(key: string): any {
    const storedValue = localStorage.getItem(key);
    
    if (storedValue !== null) {
        try {
            return JSON.parse(storedValue);
        } catch (error) {
            console.error(`Error parsing JSON for key "${key}":`, error);
            return null; // or throw the error, depending on your preference
        }
    }

    return null;
}
