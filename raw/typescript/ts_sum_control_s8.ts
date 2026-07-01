function sumArray(nums: number[]): number {
    let total = 0;
    for (let i = 0; i < nums.length; i++) {
        total += nums[i];
    }
    return total;
}

// Test the function with some data points
console.log(sumArray([1, 2, 3])); // Output: 6
console.log(sumArray([-1, -2, -3])); // Output: -6
console.log(sumArray([])); // Output: 0
