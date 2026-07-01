async function fetchJson(url: string): Promise<any> {
    try {
        const response = await fetch(url);
        
        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse the JSON body
        const jsonBody = await response.json();
        
        return jsonBody;
    } catch (error) {
        console.error('Error fetching JSON:', error);
        throw error; // Rethrow the error to handle it further up the call stack
    }
}

// Example usage:
fetchJson('https://api.example.com/data')
    .then(data => {
        console.log('Fetched data:', data);
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });
