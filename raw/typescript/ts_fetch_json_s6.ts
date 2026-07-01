async function fetchJson(url: string): Promise<any> {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching JSON:', error);
        throw error;
    }
}

// Example usage:
(async () => {
    try {
        const data = await fetchJson('https://api.example.com/data');
        console.log(data);
    } catch (error) {
        console.error(error);
    }
})();
