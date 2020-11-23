#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // User´s input
    int h;
    do
    {
        h = get_int("Height [1 to 8]: ");
    }
    while (h > 8 || h < 1);
    
    // Mario hashes
    for (int i = h; i > 0; i--)
    {
        for (int js = i - 1; js > 0; js--)
        {
            printf(" ");
        }
        for (int jh = i; jh <= h; jh++)
        {
            printf("#");
        }
    printf("\n");
    }
}