/**
 * Calculates the sum of all elements in an array.
 * @param nums An array of numbers to be summed.
 * @returns The sum of the elements in the array.
 */
function sumArray(nums: number[]): number {
    return nums.reduce((acc, curr) => acc + curr, 0);
}

// Example usage:
const result = sumArray([1, 2, 3, 4]);
console.log(result); // Output: 10
