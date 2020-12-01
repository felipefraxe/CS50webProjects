#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
    
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Forensic image\n");
        return 1;
    }
    
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Something went wrong\n");
        return 1;
    }
    
    BYTE bytes[512];
    char newf[8];
    FILE *img;
    int c = 0;
    
    while (fread(bytes, sizeof(BYTE), 512, file) > 0)
    {
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            if (c != 0)
            {
                fclose(img);
            }
        
            sprintf(newf, "%03i", c);
            img = fopen(newf, "w");
            c++;
        }
        fwrite(bytes, sizeof(BYTE), 512, img);
    }
    fclose(img);
    fclose(file);
    return 0;
}