// code1
#include <stdio.h>
#include <string.h>

// Function to find the minimum of three integers
int min(int a, int b, int c) {
    if (a < b) {
        return (a < c) ? a : c;  // If a is the smallest
    } else {
        return (b < c) ? b : c;  // If b is the smallest
    }
}

// Function to calculate the edit distance between two strings
int editDistance(char* str1, char* str2) {
    int m = strlen(str1);  // Length of the first string
    int n = strlen(str2);  // Length of the second string

    // Create a 2D array to store the edit distances
    int dp[1000][1000];  // Assuming maximum string length is 1000

    // Initialize the dp table
    for (int i = 0; i <= m; ++i) {
        for (int j = 0; j <= n; ++j) {
            if (i == 0)
                dp[i][j] = j; // If str1 is empty, insert all characters of str2
            else if (j == 0)
                dp[i][j] = i; // If str2 is empty, remove all characters of str1
            else if (str1[i - 1] == str2[j - 1])
                dp[i][j] = dp[i - 1][j - 1]; // If last characters are the same, no new operation needed
            else
                // Consider all possible operations: remove, insert, replace
                dp[i][j] = 1 + min(dp[i - 1][j],    // Remove
                                   dp[i][j - 1],    // Insert
                                   dp[i - 1][j - 1] // Replace
                                  );
        }
    }

    // Return the edit distance from the bottom-right cell of the DP table
    return dp[m][n];
}

// Main function to test the edit distance function
int main() {
    char s[1000], t[1000];  // Arrays to hold the input strings
    scanf("%s %s", s, t);  // Input two strings
    int ans = editDistance(s, t);  // Calculate the edit distance
    printf("%d\n", ans);  // Output the result

    return 0;
}

// code2(dissimilar)

#include <stdio.h>
#include <string.h>

// Function to compute the minimum number of operations required to convert str1 to str2
int minOperations(char* source, char* target) {
    int lenSource = strlen(source);
    int lenTarget = strlen(target);

    // Create a 2D array to store the results
    int table[lenSource + 1][lenTarget + 1];

    // Initialize the first row and column
    for (int i = 0; i <= lenSource; i++) {
        for (int j = 0; j <= lenTarget; j++) {
            // If the source string is empty, we need to insert all characters of the target
            if (i == 0) {
                table[i][j] = j;
            }
            // If the target string is empty, we need to remove all characters of the source
            else if (j == 0) {
                table[i][j] = i;
            }
            else {
                // If characters match, no operation is needed, so we carry forward the result
                if (source[i - 1] == target[j - 1]) {
                    table[i][j] = table[i - 1][j - 1];
                }
                // Otherwise, we perform the minimum of insert, delete, or replace operation
                else {
                    int insert = table[i][j - 1];    // Insert character into source
                    int delete = table[i - 1][j];    // Delete character from source
                    int replace = table[i - 1][j - 1]; // Replace character in source

                    // Take the minimum operation and add 1 for the current operation
                    table[i][j] = 1 + (insert < delete ? (insert < replace ? insert : replace) : (delete < replace ? delete : replace));
                }
            }
        }
    }

    // The value in the bottom-right corner of the table is the final result
    return table[lenSource][lenTarget];
}

int main() {
    char firstString[1000], secondString[1000]; // Arrays to hold input strings

    // Take two string inputs
    scanf("%s %s", firstString, secondString);

    // Calculate the minimum number of operations (edit distance)
    int result = minOperations(firstString, secondString);

    // Output the result
    printf("%d\n", result);

    return 0;
}
