
// code1
#include <stdio.h>
#include <string.h>

void longestPalindrome(char* s, char* res) {
    int len = 0;
    int n = strlen(s);

    for (int i = 0; i < n; i++) {
        // Check for odd-length palindromes centered at i
        int l = i, r = i;
        while (l >= 0 && r < n && s[l] == s[r]) {
            if (r - l + 1 > len) {
                len = r - l + 1;
                strncpy(res, s + l, len);
                res[len] = '\0'; // Null-terminate the result
            }
            l--;
            r++;
        }

        // Check for even-length palindromes centered at i and i + 1
        l = i;
        r = i + 1;
        while (l >= 0 && r < n && s[l] == s[r]) {
            if (r - l + 1 > len) {
                len = r - l + 1;
                strncpy(res, s + l, len);
                res[len] = '\0'; // Null-terminate the result
            }
            l--;
            r++;
        }
    }
}

int main() {
    char s[1000];
    char res[1000] = ""; // Initialize result array with empty string
    scanf("%s", s);

    longestPalindrome(s, res);
    printf("%s\n", res);

    return 0;
}

// code2(dissimilar)

#include <stdio.h>
#include <string.h>

// Memoization table
int dp[1000][1000];

// Helper function to check if a substring input[i...j] is a palindrome
int isPalindrome(char* input, int i, int j) {
    if (i >= j) return 1;  // A single character or empty substring is a palindrome
    if (dp[i][j] != -1) return dp[i][j];  // If already calculated, return the cached result
    
    if (input[i] == input[j]) {
        dp[i][j] = isPalindrome(input, i + 1, j - 1);  // Recur for the inner substring
    } else {
        dp[i][j] = 0;  // Not a palindrome
    }
    
    return dp[i][j];
}

// Function to find the longest palindromic substring
void findLongestPalindrome(char* input, char* result) {
    int n = strlen(input);
    int maxLength = 1;  // Start with a minimum palindrome of length 1
    int start = 0;  // Start index of the longest palindrome
    
    // Initialize the memoization table with -1 (indicating not calculated)
    memset(dp, -1, sizeof(dp));
    
    // Iterate through all possible substrings
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            // Check if the substring input[i...j] is a palindrome
            if (isPalindrome(input, i, j)) {
                int length = j - i + 1;
                // If it's the longest palindrome found so far, update the result
                if (length > maxLength) {
                    maxLength = length;
                    start = i;
                }
            }
        }
    }
    
    // Extract the longest palindromic substring
    strncpy(result, input + start, maxLength);
    result[maxLength] = '\0';  // Null-terminate the result string
}

int main() {
    char input[1000];
    char result[1000] = "";

    scanf("%s", input);

    findLongestPalindrome(input, result);
    printf("%s\n", result);

    return 0;
}
