/**
 * Sums an array of numbers.
 * 
 * @param nums - An array of numbers to be summed.
 * @returns The sum of the numbers in the array.
 */
function sumArray(nums: number[]): number {
    return nums.reduce((acc, curr) => acc + curr, 0);
}

// Check function to verify the correctness of the sumArray function
function checkSumArray() {
    console.assert(sumArray([1, 2, 3]) === 6, 'Test case 1 failed');
    console.assert(sumArray([-1, -2, -3]) === -6, 'Test case 2 failed');
    console.assert(sumArray([0, 0, 0]) === 0, 'Test case 3 failed');
    console.assert(sumArray([]) === 0, 'Test case 4 failed');
    console.log('All test cases passed!');
}

// Run the check function to verify the solution
checkSumArray();
