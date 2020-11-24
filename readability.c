#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string txt);
int count_words(string txt);
int count_sentences(string txt);

int main(void)
{
    string text = get_string("Text: ");
    int cl = count_letters(text);
    int cw = count_words(text);
    int cs = count_sentences(text);
    float L = (float) cl / cw * 100;
    float S = (float) cs / cw * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string txt)
{
    int c = 0;
    for (int i = 0, n = strlen(txt); i < n; i++)
    {
        if (isalpha(txt[i]))
        {
            c++;
        }
    }
    return c;
}

int count_words(string txt)
{
    int c = 1;
    for (int i = 0, n = strlen(txt); i < n; i++)
    {
        if (isspace(txt[i]))
        {
            c++;
        }
    }
    return c;
}

int count_sentences(string txt)
{
    int c = 0;
    for (int i = 0, n = strlen(txt); i < n; i++)
    {
        if ((char) txt[i] == (char) '.' || (char) txt[i] == (char) '?' || (char) txt[i] == (char) '!')
        {
            c++;
        }
    }
    return c;
}