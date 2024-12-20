
//code1
#include <stdio.h>

int memo[1000] = {0}; // Memoization array to store previously computed results

int countWays(int steps) {
    if (steps <= 0) return 0;
    if (steps == 1) return 1;
    if (steps == 2) return 2;

    if (memo[steps] != 0) return memo[steps]; // Use cached result if available

    memo[steps] = countWays(steps - 1) + countWays(steps - 2);
    return memo[steps];
}

int main() {
    int steps;
    scanf("%d", &steps);

    int totalWays = countWays(steps);
    printf("%d\n", steps, totalWays);

    return 0;
}

//code2(dissimilar)

#include <stdio.h>

int calculateWays(int total) {
    if (total <= 0) return 0;
    if (total == 1) return 1;
    if (total == 2) return 2;

    int dp[total + 1]; // Array to store ways to reach each step
    dp[0] = 0;
    dp[1] = 1;
    dp[2] = 2;

    for (int i = 3; i <= total; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    
    return dp[total];
}

int main() {
    int total;
    scanf("%d", &total);

    int ways = calculateWays(total);
    printf("%d\n", ways);

    return 0;
}

//code3(similar):
#include <stdio.h>

int climbStairs(int n) {
    if(n <= 0) return 0;
    if(n == 1) return 1;
    if(n == 2) return 2;
    
    int x = 2;
    int y = 1;
    int res = 0;
    
    for(int i = 3; i <= n; i++) {
        res = x + y;
        y = x;
        x = res;
    }
    return res;
}

int main() {
    int n;
    scanf("%d", &n);
    
    int result = climbStairs(n);
    printf("%d\n", result);

    return 0;
}