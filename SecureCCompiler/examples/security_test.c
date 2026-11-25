#include <stdio.h>
#include <string.h>

int main()
{
    char name[10];
    char user_input[] = "Hello";
    char password[] = "admin123";

    gets(name);

    strcpy(name, "Hello");

    sprintf(name, "Hello World");

    printf(user_input);

    return 0;
}
