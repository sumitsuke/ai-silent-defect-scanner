// Function to calculate the sum of an array of numbers
function sumArray(nums: number[]): number {
    // Initialize the sum variable to zero
    let sum = 0;
    
    // Iterate through each number in the array
    for (let i = 0; i < nums.length; i++) {
        // Add each number to the sum
        sum += nums[i];
    }
    
    // Return the calculated sum
    return sum;
}

// Example usage:
const numbers = [1, 2, 3, 4, 5];
console.log(sumArray(numbers)); // Output: 15
