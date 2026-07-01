function parseIntField(obj: Record<string, string>, key: string): number | undefined {
    if (obj.hasOwnProperty(key) && !isNaN(parseInt(obj[key], 10))) {
        return parseInt(obj[key], 10);
    } else {
        return undefined;
    }
}
