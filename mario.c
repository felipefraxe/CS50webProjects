#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height[1-8]: ");
    }
    while(height < 1 || height > 8);
    
    int cl = 0;
    int cg = height - 1;
    for (int i = 0; i < height; i++)
    {
        for (int j = height - 1; j > cl; j--)
        {
            printf(" ");
        }
        
        for (int k = 0; k <= cl; k++)
        {
            printf("#");
        }
        
        printf("  ");
        
        for (int l = 0; l <= cl; l++)
        {
            printf("#");
        }
    printf("\n");
    cl++;
    }
}