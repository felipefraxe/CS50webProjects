#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int check_argv(string x);

int main(int argc, string argv[])
{
    int c = check_argv(argv[1]);
    if (argc == 2 && c == strlen(argv[1]))
    {
        int key = atoi(argv[1]);
        string pt = get_string("plaintext: ");
        printf("ciphertext: ");
            
        while (key >= 26)
        {
            key -= 26;
        }
            
        for (int i = 0, n = strlen(pt); i < n; i++)
        {
            if (pt[i] >= 'a' && pt[i] <= 'z')
            {
                if (pt[i] + key > 122)
                {
                    printf("%c", pt[i] + key - 26);
                }

                else
                {
                    printf("%c", (pt[i] + key));
                }
            }
                
            else if (pt[i] >= 'A' && pt[i] <= 'Z')
            {
                if (pt[i] + key > 90)
                {
                    printf("%c", pt[i] + key - 26);
                }

                else
                {
                    printf("%c", (pt[i] + key));
                }
            }
        
            else
            {
                printf("%c", pt[i]);
            }
                
        }
        printf("\n");
        }
        
        else
        {
            printf("key\n");
            return 1;
        }
    }
    
    
    else
    {
        printf("key\n");
        return 1; 
    }
}

int check_argv(string x)
{
    int c = 0;
    for (int i = 0, n = strlen(x); i < n; i++)
    {
        if (isdigit(x[i]))
        {
            c ++;
        }
    }
    return c;
}