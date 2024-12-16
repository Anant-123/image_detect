import streamlit as st
from PIL import Image
import numpy as np
import cv2
from streamlit_drawable_canvas import st_canvas

# Function to crop the image based on rectangle coordinates
def crop_image_with_coords(image, x1, y1, x2, y2):
    cropped_image = image[y1:y2, x1:x2]
    return cropped_image

# Main Streamlit app
def main():
    st.title("Billets Counting Application with Interactive Cropping")
    
    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        image_np = np.array(image)  # Convert to NumPy array (for OpenCV operations)

        # Display the original image
        st.subheader("Original Image")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Interactive cropping section
        st.subheader("Interactive Cropping")
        st.write("Draw a rectangle to crop the desired area of the image.")
        
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Transparent orange fill for rectangle
            stroke_width=2,
            stroke_color="blue",  # Outline color
            background_image=Image.open(uploaded_file)  # Background is the uploaded image
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode="rect",  # Rectangle drawing mode
            key="crop_canvas",
        )

        # Check if a rectangle was drawn
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            if len(objects) > 0:
                # Extract coordinates of the rectangle
                rect_coords = objects[-1]  # Use the last drawn rectangle
                x1, y1, width, height = (
                    int(rect_coords["left"]),
                    int(rect_coords["top"]),
                    int(rect_coords["width"]),
                    int(rect_coords["height"]),
                )
                x2, y2 = x1 + width, y1 + height

                # Crop the image based on rectangle coordinates
                cropped_image = crop_image_with_coords(image_np, x1, y1, x2, y2)

                # Display the cropped image
                st.subheader("Cropped Image")
                st.image(cropped_image, caption="Cropped Image", use_column_width=True)

                # Reference Circle Section
                st.subheader("Reference Circle Selection")
                radius = (width + height) // 4
                st.write(f"Estimated Reference Circle Radius: {radius} pixels")

                # Detect Billets
                st.subheader("Detect Billets")
                if st.button("Detect"):
                    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

                    circles = cv2.HoughCircles(
                        blurred,
                        cv2.HOUGH_GRADIENT,
                        dp=1.2,
                        minDist=radius * 1.5,
                        param1=50,
                        param2=30,
                        minRadius=int(radius * 0.8),
                        maxRadius=int(radius * 1.2),
                    )

                    if circles is not None:
                        circles = np.round(circles[0, :]).astype("int")
                        for (x, y, r) in circles:
                            cv2.circle(cropped_image, (x, y), r, (0, 255, 0), 2)

                        st.image(cropped_image, caption="Billets Detected", use_column_width=True)
                        st.success(f"Number of Billets Detected: {len(circles)}")
                    else:
                        st.warning("No Billets Detected")

# Run the Streamlit app
if __name__ == "__main__":
    main()
