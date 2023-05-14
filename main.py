import streamlit as st
import cv2
import numpy as np
import dijkstra
import helpers
import time

# Start Buildin the Ui
# set a title for the page
st.title('Maze Solver')

# Create an Image Upload Button
uploaded_file = st.file_uploader("Choose an image", ["jpg", "jpeg", "png"])

st.write('Or')
# Handle the case if the user don't have images allow him to use the default
use_default_image = st.checkbox('Use default maze')
opencv_image = None
marked_image = None

# Read the image if it is the default or if the user upload one
if use_default_image:
    opencv_image = cv2.imread('defaultMaze.png')

elif uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

# Start processing the image
if opencv_image is not None:
    # Allow user to choose the start and finish points using sliders
    st.subheader(
        'Use the sliders on the right to position the start and end points')
    start_x = st.sidebar.slider("Start X", value=26 if use_default_image else 50,
                                min_value=0, max_value=opencv_image.shape[1], key='sx')
    start_y = st.sidebar.slider("Start Y", value=6 if use_default_image else 100,
                                min_value=0, max_value=opencv_image.shape[0], key='sy')
    finish_x = st.sidebar.slider("Finish X", value=9 if use_default_image else 100,
                                 min_value=0, max_value=opencv_image.shape[1], key='fx')
    finish_y = st.sidebar.slider("Finish Y", value=221 if use_default_image else 100,
                                 min_value=0, max_value=opencv_image.shape[0], key='fy')
    marked_image = opencv_image.copy()
    # ui circle thickness based on img size
    circle_thickness = (marked_image.shape[0]+marked_image.shape[0])//2//100
    cv2.circle(marked_image, (start_x, start_y),
               circle_thickness, (0, 255, 0), -1)
    cv2.circle(marked_image, (finish_x, finish_y),
               circle_thickness, (255, 0, 0), -1)
    st.image(marked_image, channels="RGB", width=800)

# Solve maze , draw the solution and render it to the UI
start = time.time()
if marked_image is not None:
    if st.button('Solve Maze'):
        with st.spinner('Solving your maze'):
            path = dijkstra.find_shortest_path(
                opencv_image, (start_x, start_y), (finish_x, finish_y))
            pathed_image = opencv_image.copy()
            helpers.drawPath(pathed_image, path, 2)
            st.image(pathed_image, channels="RGB", width=800)
end = time.time()
print('Time elapsed is : {} ms'.format((end-start)//1))
