# ImageBorders
A simple standalone program to add borders to finished edits. It is intended to support jpg files and export as jpg. The idea is you have already exported your jpgs for general use after editing.

I could not find a free lightweight, standalone program that simply just allowed me to add a 1:1 border to my images so I could upload to Instagram and retain my full image for view on the feed.
Although I learned some programming at college I never pursued it later in life so I wasn't capable of making this quickly myself. I emplyed the help of ChatGPT to do the heavy lifting so I could get to the end product. Therefore most of this code is AI generated, I simply gave it heavy direction on what I needed and helping with extnesive debugging. This project was for personal use but I want to just put it out there for others who are looking for something similar. I have ironed out any bugs I have found in testing, and it seems to work as I intend it to. 
It is not very feature rich as it is only intended to add a border to your image. It is also capable of resizing your image and setting a jpg quality for file size limits.

I will likely work on further features as a hobby but right now it is missing border colours, image preview, loading bars and a check to make sure you don't want to overwrite existing files. For my purpose this is not an issue for me. I have not tested for extreme resize dimensions as I want to keep that section free for users to input what they want, even though extreme dimensions could adversly affect your system when generating large files.



Instructions for use.
1. Import photos. This can be any amount but not 0.
2. Select your aspect ratio for the white border. This will always default to current image aspect ratio. There is an option for custome ratios which you simply enter numbers into a pop up prompt.
3. Set border width. This will always default to 0 on start up.
4. Resize Max Dimensions. This will default to 1080 on start up. You can input any number and it will make the longest edge to the pixel value you want and resize the short edge to maintain aspect ratio.
5. JPG quality. You can only select between 1 and 100. If you go above or below it well default to 1 or 100 on export. This will always default to 90 on start up.
6. Export images. Simply allows you to select a destination before exporting.
