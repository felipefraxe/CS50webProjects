#include <stdio.h>
#include <stdlib.h>

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
    
    int c = 0;
    unsigned char bytes[512];
    char newf[8];
    char image[512];
    FILE *img = fopen(newf, "w");
    
    for(int i = 0; i < 2048; i++)
    {
        fread(bytes, 512, 1, file);
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            c++;
            if (c == 1)
            {
                sprintf(newf, "%03i.jpg", c);
                fwrite(image, 512, 1, img);
            }

            else
            {
                fclose(img);
                sprintf(newf, "%03i.jpg", c);
                fwrite(image, 512, 1, img);
            }
        }
        
        else if (c > 1)
        {
            fwrite(image, 512, 1, img);
        }
    }
}