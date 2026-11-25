#include<stdio.h>

int main()
{
    char name;
    char username;
    char password;
    char message;

    int age = 19;
    int mark1 = 85;
    int mark2 = 90;
    int mark3 = 75;
    int total;
    int average;

    password = "student123";

    printf("STUDENT LOGIN SYSTEM\n");
    printf("--------------------\n");

    printf("Enter student name: ");
    gets(name);

    printf("Enter username: ");
    gets(username);

    printf("Student Details\n");
    printf("Age: %d\n", age);

    strcpy(message, name);

    sprintf(message, "Welcome");

    printf(message);

    total = mark1 + mark2 + mark3;
    average = total / 3;

    printf("\nMARK DETAILS\n");
    printf("Mark 1: %d\n", mark1);
    printf("Mark 2: %d\n", mark2);
    printf("Mark 3: %d\n", mark3);

    printf("Total: %d\n", total);
    printf("Average: %d\n", average);

    if (average >= 90)
    {
        printf("Grade: A\n");
    }
    else if (average >= 75)
    {
        printf("Grade: B\n");
    }
    else if (average >= 50)
    {
        printf("Grade: C\n");
    }
    else
    {
        printf("Grade: Fail\n");
    }

    printf("Login completed.\n");

    return 0;
}