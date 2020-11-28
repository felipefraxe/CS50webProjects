#include <math.h>
#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round(((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / (float) 3));
            
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            
            int sepiaGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            
            int sepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int c = 1;
        int tempr;
        int tempg;
        int tempb;
        for (int j = 0; j < floor(width / 2); j++)
        {
            tempr = image[i][j].rgbtRed;
            tempg = image[i][j].rgbtGreen;
            tempb = image[i][j].rgbtBlue;
            image[i][j].rgbtRed = image[i][width - c].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - c].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - c].rgbtBlue;
            image[i][width - c].rgbtRed = tempr;
            image[i][width - c].rgbtGreen = tempg;
            image[i][width - c].rgbtBlue = tempb;
            c++;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE average[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (i == 0) 
            {
                if (j == 0)
                {
                    average[i][j].rgbtRed = round((image[i][j].rgbtRed + image[i + 1][j].rgbtRed +
                                                   image[i][j + 1].rgbtRed + image[i + 1][j + 1].rgbtRed) / (float) 4);
                    
                    average[i][j].rgbtGreen = round((image[i][j].rgbtGreen + image[i + 1][j].rgbtGreen +
                                                     image[i][j + 1].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / (float) 4);
                    
                    average[i][j].rgbtBlue = round((image[i][j].rgbtBlue + image[i + 1][j].rgbtBlue +
                                                    image[i][j + 1].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / (float) 4);
                }
                
                else if (j == width - 1)
                {
                    average[i][j].rgbtRed = round((image[i][j].rgbtRed + image[i + 1][j].rgbtRed +
                                                   image[i][j - 1].rgbtRed + image[i + 1][j - 1].rgbtRed) / (float) 4);
                    
                    average[i][j].rgbtGreen = round((image[i][j].rgbtGreen + image[i + 1][j].rgbtGreen +
                                                     image[i][j - 1].rgbtGreen + image[i + 1][j - 1].rgbtGreen) / (float) 4);
                    
                    average[i][j].rgbtBlue = round((image[i][j].rgbtBlue + image[i + 1][j].rgbtBlue +
                                                    image[i][j - 1].rgbtBlue + image[i + 1][j - 1].rgbtBlue) / (float) 4);
                }
                
                else
                {
                    average[i][j].rgbtRed = round((image[i][j - 1].rgbtRed + image[i][j].rgbtRed + image[i][j + 1].rgbtRed +
                                                   image[i + 1][j - 1].rgbtRed + image[i + 1][j].rgbtRed + 
                                                   image[i + 1][j + 1].rgbtRed) / (float) 6);
        
                    average[i][j].rgbtGreen = round((image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen +
                                                     image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / (float) 6);
                
                    average[i][j].rgbtBlue = round((image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue +
                                                    image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / (float) 6);
                }
            }
            
            else if (i == height - 1)
            {
                if (j == 0)
                {
                    average[i][j].rgbtRed = round((image[i][j].rgbtRed + image[i - 1][j].rgbtRed + 
                                                   image[i][j + 1].rgbtRed + image[i - 1][j + 1].rgbtRed) / (float) 4);
                    
                    average[i][j].rgbtGreen = round((image[i][j].rgbtGreen + image[i - 1][j].rgbtGreen +
                                                     image[i][j + 1].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / (float) 4);
                    
                    average[i][j].rgbtBlue = round((image[i][j].rgbtBlue + image[i - 1][j].rgbtBlue +
                                                    image[i][j + 1].rgbtBlue + image[i - 1][j + 1].rgbtBlue) / (float) 4);
                }

                else if (j == width - 1)
                {
                    average[i][j].rgbtRed = round((image[i][j].rgbtRed + image[i - 1][j].rgbtRed +
                                                   image[i][j - 1].rgbtRed + image[i - 1][j - 1].rgbtRed) / (float) 4);
                    
                    average[i][j].rgbtGreen = round((image[i][j].rgbtGreen + image[i - 1][j].rgbtGreen + 
                                                     image[i][j - 1].rgbtGreen + image[i - 1][j - 1].rgbtGreen) / (float) 4);
                    
                    average[i][j].rgbtBlue = round((image[i][j].rgbtBlue + image[i - 1][j].rgbtBlue +
                                                    image[i][j - 1].rgbtBlue + image[i - 1][j - 1].rgbtBlue) / (float) 4);
                }
                
                else
                {
                    average[i][j].rgbtRed = round((image[i][j - 1].rgbtRed + image[i][j].rgbtRed + image[i][j + 1].rgbtRed +
                                                   image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed) / (float) 6);
                
                    average[i][j].rgbtGreen = round((image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen +
                                                     image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen) / (float) 6);
                
                    average[i][j].rgbtBlue = round((image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue +
                                                    image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue) / (float) 6);
                }
            }
            
            else if (j == 0)
            {
                average[i][j].rgbtRed = round((image[i - 1][j].rgbtRed + image[i][j].rgbtRed + image[i + 1][j].rgbtRed +
                                               image[i - 1][j + 1].rgbtRed + image[i][j + 1].rgbtRed + image[i + 1][j + 1].rgbtRed) / (float) 6);
            
                average[i][j].rgbtGreen = round((image[i - 1][j].rgbtGreen + image[i][j].rgbtGreen + image[i + 1][j].rgbtGreen +
                                                 image[i - 1][j + 1].rgbtGreen + image[i][j + 1].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / (float) 6);
                
                average[i][j].rgbtBlue = round((image[i - 1][j].rgbtBlue + image[i][j].rgbtBlue + image[i + 1][j].rgbtBlue +
                                                image[i - 1][j + 1].rgbtBlue + image[i][j + 1].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / (float) 6);
            }

            else if (j == width - 1)
            {
                average[i][j].rgbtRed = round((image[i - 1][j].rgbtRed + image[i][j].rgbtRed + image[i + 1][j].rgbtRed +
                                               image[i - 1][j - 1].rgbtRed + image[i][j - 1].rgbtRed + image[i + 1][j - 1].rgbtRed) / (float) 6);
                
                average[i][j].rgbtGreen = round((image[i - 1][j].rgbtGreen + image[i][j].rgbtGreen + image[i + 1][j].rgbtGreen +
                                                 image[i - 1][j - 1].rgbtGreen + image[i][j - 1].rgbtGreen + image[i + 1][j - 1].rgbtGreen) / (float) 6);
                
                average[i][j].rgbtBlue = round((image[i - 1][j].rgbtBlue + image[i][j].rgbtBlue + image[i + 1][j].rgbtBlue +
                                                image[i - 1][j - 1].rgbtBlue + image[i][j - 1].rgbtBlue + image[i + 1][j - 1].rgbtBlue) / (float) 6);
            }
            
            else
            {
                average[i][j].rgbtRed = round((image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed +
                                               image[i][j - 1].rgbtRed + image[i][j].rgbtRed + image[i][j + 1].rgbtRed +
                                               image[i + 1][j - 1].rgbtRed + image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / (float) 9);
            
                average[i][j].rgbtGreen = round((image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen +
                                                 image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen +
                                                 image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / (float) 9);
            
                average[i][j].rgbtBlue = round((image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue +
                                                image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue +
                                                image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / (float) 9);
            }
        }
    }
    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < width; b++)
        {
            image[a][b].rgbtRed = average[a][b].rgbtRed;
            image[a][b].rgbtGreen = average[a][b].rgbtGreen;
            image[a][b].rgbtBlue = average[a][b].rgbtBlue;
        }
    }
    return;
}
