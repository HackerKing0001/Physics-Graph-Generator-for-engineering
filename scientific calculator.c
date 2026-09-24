#include <stdio.h>
#include <math.h>

int main() {
    int choice, n, i;
    double a, b, result;

    do {
        printf("\n===== SCIENTIFIC CALCULATOR =====\n");
        printf("1. Addition\n");
        printf("2. Subtraction\n");
        printf("3. Multiplication\n");
        printf("4. Division\n");
        printf("5. Power (a^b)\n");
        printf("6. Square Root\n");
        printf("7. Sin\n");
        printf("8. Cos\n");
        printf("9. Tan\n");
        printf("10. Log (base 10)\n");
        printf("11. Natural Log (ln)\n");
        printf("12. Factorial\n");
        printf("13. Exit\n");

        printf("\nEnter your choice: ");
        scanf("%d", &choice);

        switch (choice) {

            case 1:
                printf("Enter two numbers: ");
                scanf("%lf %lf", &a, &b);
                printf("Result = %.2lf\n", a + b);
                break;

            case 2:
                printf("Enter two numbers: ");
                scanf("%lf %lf", &a, &b);
                printf("Result = %.2lf\n", a - b);
                break;

            case 3:
                printf("Enter two numbers: ");
                scanf("%lf %lf", &a, &b);
                printf("Result = %.2lf\n", a * b);
                break;

            case 4:
                printf("Enter two numbers: ");
                scanf("%lf %lf", &a, &b);

                if (b != 0)
                    printf("Result = %.2lf\n", a / b);
                else
                    printf("Error! Division by zero.\n");

                break;

            case 5:
                printf("Enter base and exponent: ");
                scanf("%lf %lf", &a, &b);
                printf("Result = %.2lf\n", pow(a, b));
                break;

            case 6:
                printf("Enter a number: ");
                scanf("%lf", &a);

                if (a >= 0)
                    printf("Square Root = %.2lf\n", sqrt(a));
                else
                    printf("Error! Cannot find square root of a negative number.\n");

                break;

            case 7:
                printf("Enter angle in degrees: ");
                scanf("%lf", &a);
                result = sin(a * 3.14159265 / 180);
                printf("Sin(%.2lf) = %.4lf\n", a, result);
                break;

            case 8:
                printf("Enter angle in degrees: ");
                scanf("%lf", &a);
                result = cos(a * 3.14159265 / 180);
                printf("Cos(%.2lf) = %.4lf\n", a, result);
                break;

            case 9:
                printf("Enter angle in degrees: ");
                scanf("%lf", &a);
                result = tan(a * 3.14159265 / 180);
                printf("Tan(%.2lf) = %.4lf\n", a, result);
                break;

            case 10:
                printf("Enter a positive number: ");
                scanf("%lf", &a);

                if (a > 0)
                    printf("log10(%.2lf) = %.4lf\n", a, log10(a));
                else
                    printf("Error! Number must be positive.\n");

                break;

            case 11:
                printf("Enter a positive number: ");
                scanf("%lf", &a);

                if (a > 0)
                    printf("ln(%.2lf) = %.4lf\n", a, log(a));
                else
                    printf("Error! Number must be positive.\n");

                break;

            case 12:
                printf("Enter a positive integer: ");
                scanf("%d", &n);

                if (n >= 0) {
                    result = 1;

                    for (i = 1; i <= n; i++)
                        result = result * i;

                    printf("%d! = %.0lf\n", n, result);
                } else {
                    printf("Error! Factorial cannot be negative.\n");
                }

                break;

            case 13:
                printf("Calculator closed.\n");
                break;

            default:
                printf("Invalid choice! Try again.\n");
        }

    } while (choice != 13);

    return 0;
}