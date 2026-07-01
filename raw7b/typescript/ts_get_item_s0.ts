function getItem(key: string): any | null {
    try {
        const storedValue = localStorage.getItem(key);
        if (storedValue === null) {
            return null;
        }
        return JSON.parse(storedValue);
    } catch (error) {
        console.error(`Error parsing localStorage item with key "${key}":`, error);
        return null;
    }
}

// Example usage:
const myData = getItem('myKey');
console.log(myData);
