# OCR API for Web Service

Add this line to your python web application startup script

```
import OCRapi
```

# Doc 

## Functions

- dirOCR(dirpath)

        do ocr operation on specific directory    
        return a list contains tuples which likes (filename,ocrresultstring)

- fileOCR(imagePath)

        do ocr operations on a single image file
        return a single string of ocr result
        lines split by '\n'
- imgArrOCR(image)

        do ocr operations on a single image numpy array
        return a single string of ocr result
        lines split by '\\n'

## Attention!

Weights are omitted in this repo.
    