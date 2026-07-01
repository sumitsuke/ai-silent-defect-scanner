function sumArray(nums: number[]): number {
    return nums.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
}

// Example usage:
const result = sumArray([1, 2, 3, 4, 5]);
console.log(result); // Output: 15
