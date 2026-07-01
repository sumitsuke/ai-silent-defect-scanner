function getItem(key: string): any {
    const item = localStorage.getItem(key);
    
    if (item) {
        return JSON.parse(item);
    }

    return null;
}
