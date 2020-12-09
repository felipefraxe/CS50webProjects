// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "dictionary.h"
#include <string.h>
#include <strings.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const int N = 'z' * (LENGTH + 1);

// Hash table
node *table[N];

int cwords = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int i = hash(word);
  
    node *cursor = table[i];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return (sum % N);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    
    char read[LENGTH + 1];
    
    while (fscanf(file, "%s", read) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        
        strcpy(n->word, read);
        n->next = NULL;
        
        int i = hash(read);
        
        if (table[i] != NULL)
        {
            n->next = table[i];
        }
        
        table[i] = n;
        
        cwords++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return cwords;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor;
    node *tmp;
    
    for (int i = 0; i < N; i++)
    { 
        tmp = table[i];
        cursor = table[i];
        
        while(cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
