#ifndef __STACK__
#define __STACK__

#ifdef __cplusplus
extern "C"
{
#endif
#include <stdlib.h>
#include <inttypes.h>


    typedef struct Response {
        int status;
        size_t len;
        const char * dataType;
        void * data;
    } Response;


    typedef struct CMat {
        void* mat;
    } CMat;

    typedef struct CPixels {
        unsigned char* pixels;
        size_t len;
    } CPixels;

    typedef struct Image
    {
        uint8_t *pixels;
        float exposure; 
        uint32_t x0;
        uint32_t x1;
        uint32_t y0;
        uint32_t y1;
        size_t len;
    } Image;

    typedef struct Buffer {
        uint8_t* data;
        size_t len;
    } Buffer;

    Response stackImages(Image *img, size_t len);
    Response grayscale(Image img);
    Response colorize(CMat img, uint8_t map);
    Response cMatToImg(CMat mat);
    CPixels getPixels(CMat mat);

#ifdef __cplusplus
}
#endif
#endif
