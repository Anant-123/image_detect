import streamlit as st
from PIL import Image
import numpy as np
import cv2

# Function to crop the image using slider values
def crop_image(image, top, bottom, left, right):
    height, width = image.shape[:2]
    cropped_image = image[int(height * top):int(height * (1 - bottom)),
                          int(width * left):int(width * (1 - right))]
    return cropped_image

# Main Streamlit app
def main():
    st.title("Billets Counting application")
    
    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        image_np = np.array(image)  # Convert to NumPy array

        # Original Image Display
        st.subheader("Original Image")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Crop the Image Section
        st.subheader("Crop the Image")
        col1, col2 = st.columns([2, 1])  # Side-by-side layout

        with col1:
            st.write("### Cropping Controls")
            top = st.slider("Top Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            bottom = st.slider("Bottom Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            left = st.slider("Left Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            right = st.slider("Right Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            cropped_image = crop_image(image_np, top, bottom, left, right)
            

        with col2:
            ref_circle = cropped_image  # Initialize reference circle image
            st.image(ref_circle, caption="Reference Circle", use_column_width=True)

        # Reference Circle Section
        st.subheader("Reference Circle Selection")
        col1, col2 = st.columns([2, 1])  # Side-by-side layout for reference circle

        with col1:
            st.write("### Reference Circle Controls")
            ref_top = st.slider("Ref. Top Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_bottom = st.slider("Ref. Bottom Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_left = st.slider("Ref. Left Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_right = st.slider("Ref. Right Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_circle = crop_image(cropped_image, ref_top, ref_bottom, ref_left, ref_right)
            

        with col2:
           st.image(ref_circle, caption="Selected Reference Circle", use_column_width=True)


        # Radius Calculation and Cylinder Detection
        #st.image(ref_circle, caption="Selected Reference Circle", use_column_width=True)
        radius = (ref_circle.shape[0] + ref_circle.shape[1]) // 4
        st.write(f"Estimated Radius: {radius} pixels")

        # Detect Cylinders
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

                st.image(cropped_image, caption="Billets Cylinders", use_column_width=True)
                st.success(f"Number of Billets Detected: {len(circles)}")
            else:
                st.warning("No Billets Detected")

# Run the Streamlit app
if __name__ == "__main__":
    main()
