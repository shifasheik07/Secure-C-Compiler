#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "security.h"


// Check whether a line contains gets()
int contains_gets(const char *line)
{
    const char *p = line;

    while ((p = strstr(p, "gets")) != NULL)
    {
        int left_ok = (p == line ||
                      (!isalnum((unsigned char)p[-1]) && p[-1] != '_'));

        const char *q = p + 4;

        int right_ok = (!isalnum((unsigned char)*q) && *q != '_');

        while (isspace((unsigned char)*q))
            q++;

        if (left_ok && right_ok && *q == '(')
            return 1;

        p += 4;
    }

    return 0;
}


// Check whether a line contains strcpy()
int contains_strcpy(const char *line)
{
    const char *p = line;

    while ((p = strstr(p, "strcpy")) != NULL)
    {
        int left_ok = (p == line ||
                      (!isalnum((unsigned char)p[-1]) && p[-1] != '_'));

        const char *q = p + 6;

        int right_ok = (!isalnum((unsigned char)*q) && *q != '_');

        while (isspace((unsigned char)*q))
            q++;

        if (left_ok && right_ok && *q == '(')
            return 1;

        p += 6;
    }

    return 0;
}

// Check whether a line contains sprintf()
int contains_sprintf(const char *line)
{
    const char *p = line;

    while ((p = strstr(p, "sprintf")) != NULL)
    {
        int left_ok = (p == line ||
                      (!isalnum((unsigned char)p[-1]) && p[-1] != '_'));

        const char *q = p + 7;

        int right_ok = (!isalnum((unsigned char)*q) && *q != '_');

        while (isspace((unsigned char)*q))
            q++;

        if (left_ok && right_ok && *q == '(')
            return 1;

        p += 7;
    }

    return 0;
}

// Check for potentially unsafe printf()
int contains_unsafe_printf(const char *line)
{
    const char *p = line;

    while ((p = strstr(p, "printf")) != NULL)
    {
        int left_ok = (p == line ||
                      (!isalnum((unsigned char)p[-1]) && p[-1] != '_'));

        const char *q = p + 6;

        while (isspace((unsigned char)*q))
            q++;

        if (left_ok && *q == '(')
        {
            q++;

            while (isspace((unsigned char)*q))
                q++;

            // A variable as the first argument may be unsafe
            if (isalpha((unsigned char)*q) || *q == '_')
                return 1;
        }

        p += 6;
    }

    return 0;
}

// Check for possible hardcoded credentials
int contains_hardcoded_secret(const char *line)
{
    const char *keywords[] = {
        "password",
        "passwd",
        "api_key",
        "secret",
        "access_token"
    };

    int count = 5;

    for (int i = 0; i < count; i++)
    {
        const char *p = strstr(line, keywords[i]);

        if (p != NULL)
        {
            const char *equal = strchr(p, '=');

            if (equal != NULL)
            {
                const char *quote = strchr(equal, '"');

                if (quote != NULL)
                    return 1;
            }
        }
    }

    return 0;
}

// Scan the C source file
int check_security(const char *filename)
{
    FILE *file = fopen(filename, "r");

    if (file == NULL)
    {
        printf("Error: Cannot open file.\n");
        return -1;
    }

    char line[2048];
    int line_number = 0;
    int warnings = 0;

    printf("\n===== SECURITY ANALYSIS =====\n");

    while (fgets(line, sizeof(line), file))
    {
        line_number++;

        // Check gets()
        if (contains_gets(line))
        {
            printf("[WARNING] Line %d: Unsafe gets() function detected.\n",
                   line_number);

            printf("          Recommendation: Use fgets() instead.\n");

            warnings++;
        }

        // Check strcpy()
        if (contains_strcpy(line))
        {
            printf("[WARNING] Line %d: Potentially unsafe strcpy() detected.\n",
                   line_number);

            printf("          Recommendation: Consider using bounded copying with proper size checks.\n");

            warnings++;
        }
        // Check sprintf()
        if (contains_sprintf(line))
        {
            printf("[WARNING] Line %d: Potentially unsafe sprintf() detected.\n",
                line_number);

            printf("          Recommendation: Consider using snprintf() with proper size checks.\n");

            warnings++;
        }
        // Check unsafe printf()
        if (contains_unsafe_printf(line))
        {
            printf("[WARNING] Line %d: Potential format string vulnerability detected.\n",
                line_number);

            printf("          Recommendation: Use printf(\"%%s\", variable) instead.\n");

            warnings++;
        }
        // Check hardcoded credentials
        if (contains_hardcoded_secret(line))
        {
            printf("[WARNING] Line %d: Possible hardcoded credential detected.\n",
                line_number);

            printf("          Recommendation: Store credentials securely outside source code.\n");

            warnings++;
        }
    }

    fclose(file);

    if (warnings == 0)
        printf("No security issues detected by current checks.\n");

    printf("\nTotal security warnings: %d\n", warnings);

    return warnings;
}
