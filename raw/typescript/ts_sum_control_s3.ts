/**
 * Calculates the sum of an array of numbers.
 * 
 * @param nums - An array of numbers to be summed.
 * @returns The sum of all numbers in the array.
 */
function sumArray(nums: number[]): number {
    return nums.reduce((acc, curr) => acc + curr, 0);
}

// Example usage:
console.log(sumArray([1, 2, 3])); // Output: 6
console.log(sumArray([-1, -2, -3])); // Output: -6
console.log(sumArray([])); // Output: 0
