function parseIntField(obj: Record<string, string>, key: string): number {
    const value = obj[key];
    if (typeof value === 'string' && !isNaN(parseInt(value))) {
        return parseInt(value);
    }
    throw new Error(`The field '${key}' does not contain a valid integer.`);
}
