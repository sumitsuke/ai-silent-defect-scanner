function parseIntField(obj: Record<string, string>, key: string): number {
  const value = obj[key];
  if (typeof value === 'string') {
    return parseInt(value, 10);
  }
  throw new Error(`Expected a string for key "${key}", but got ${value}`);
}

// Example usage:
const config: Record<string, string> = { version: "2.3.4" };
console.log(parseIntField(config, "version")); // Output: 234
