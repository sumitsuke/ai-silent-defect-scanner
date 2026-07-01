function sumArray(nums: number[]): number {
    return nums.reduce((acc, curr) => acc + curr, 0);
}

// Example usage:
const result = sumArray([1, 2, 3, 4]);
console.log(result); // Output: 10
