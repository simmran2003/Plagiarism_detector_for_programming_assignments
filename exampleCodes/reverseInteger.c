// code1
#include <stdio.h>
#include <limits.h>  // For INT_MIN and INT_MAX

int reverse(long long x) {
    long long sum = 0;
    
    while (x != 0) {
        long long last = x % 10;
        sum = (sum * 10) + last;
        x = x / 10;
    }
    
    // Check if the reversed number is within the 32-bit signed integer range
    if (sum >= INT_MIN && sum <= INT_MAX) {
        return (int)sum;  // Cast to int as the function returns an int
    } else {
        return 0;
    }
}

int main() {
    long long x;
    scanf("%lld", &x);  // Use %lld to read long long input
    
    int result = reverse(x);
    printf("%d\n", result);

    return 0;
}

// code2(dissimilar)

#include <stdio.h>
#include <stdlib.h>  // For abs() and LLONG_MIN, LLONG_MAX

// Function to reverse the digits of a number
int reverseNumber(int num) {
    int result = 0;
    int isNegative = 0;

    // Handle negative numbers
    if (num < 0) {
        isNegative = 1;
        num = -num;  // Convert to positive for processing
    }

    // Reverse the number
    while (num > 0) {
        int digit = num % 10;
        result = result * 10 + digit;
        num = num / 10;
    }

    // Reapply the negative sign if the number was negative
    if (isNegative) {
        result = -result;
    }

    // Check for integer overflow
    if (result > 2147483647 || result < -2147483648) {
        return 0;
    }

    return result;
}

int main() {
    int input;

    // Take input using scanf
    scanf("%d", &input);

    // Get the reversed number
    int reversed = reverseNumber(input);

    // Print the result
    printf("%d\n", reversed);

    return 0;
}
