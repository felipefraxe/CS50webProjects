#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    
    int count = 0;
    float o;
    do
    {
        o = get_float("Change owend: $");
    }
    while (o < 0);
    float c = round(o * 100);
    
    do
    {
        if (c >= 25)
        {
            c -= 25;
            count++;
        }
        else if (c >= 10 && c < 25)
        {
            c -= 10;
            count++;
        }
        else if (c >= 5 && c < 10)
        {
            c -= 5;
            count++;
        }
        else if (c >= 1 && c < 5)
        {
            c -= 1;
            count++;
        }
    }
    while (c != 0);
    printf("Total coins: %i\n", count);
}