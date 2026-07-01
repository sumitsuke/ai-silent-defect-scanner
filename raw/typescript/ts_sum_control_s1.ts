function sumArray(nums: number[]): number {
    let total = 0;
    for (const num of nums) {
        total += num;
    }
    return total;
}

// Example usage:
const result = sumArray([1, 2, 3, 4, 5]);
console.log(result); // Output: 15
