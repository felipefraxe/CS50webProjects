// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "dictionary.h"
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const int N = 26;

// Hash table
node *table[N];

//Temporary string
char read[LENGTH + 1];

int cwords = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *cursor;
    
    int i = hash(word);
  
    if (strcasecmp(table[i]->word, word) == 0)
    {
        return true;
    }
        
    else
    {
        cursor = table[i]->next;
        
        while (cursor != NULL)
        {
            if (strcasecmp(cursor->word, word) == 0)
            {
                return true;
            }
            
            else
            {
                cursor = cursor->next;
            }
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int i = word[0];
    return i;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    
    node *n = malloc(sizeof(node));
    if (n == NULL)
    {
        return false;
    }
    
    while (fscanf(file, "%s", read) != EOF)
    {
        strcpy(n->word, read);
        n->next = NULL;
        
        int i = hash(read);
        
        cwords++;
        
        if (table[i] != NULL)
        {
            n->next = table[i]->next;
        }
        
        table[i] = n;
    }
    size(cwords);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(int counter=0)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor;
    node *tmp;
    
    for (int i = 0; i < N; i++)
    { 
        tmp = table[i]->next;
        cursor = tmp->next;
        
        while(cursor != NULL)
        {
            free(tmp);
            tmp = cursor;
            cursor = cursor->next;
        }
    }
    return true;
}
