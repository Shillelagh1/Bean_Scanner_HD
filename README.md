# Bean_Scanner_HD /n
Scan beans at high resolution over HTTP protocol 

Python libraries used:
- bottle (for HTTP)
- numpy
- opencv-python (cv2)

Hosts a server which communicates over HTTP with a client in the Stormworks Lua API in order to generate LIDAR images of a scene.
The client may send the following requests:
- "/try/<n>", simply returns a number. For debug purposes
- "/try/<x>,<y>", previously used for debug purposes to store a new position in the image
- "/begin", sends the first position in the image. Response formatted as: "x=;y="
- "/store_NextStep\<d>", stores the distance value, "\<d>", to the current position in the image, then sends the next position in    the image. Response formatted as: "x=;y="
- "/writeOut", writes the currently stored image to "image.jpg" without interrupting the position data
- "/frame\<p>", sends either the top left (p="UL"), the top right (p="UR"), the bottom left (p="BL"), or the bottom right        (p="BR") position in the image, in order to determine if the position sent is being properly translated into angles for the   pointer
