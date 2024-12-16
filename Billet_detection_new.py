import streamlit as st
from PIL import Image
import numpy as np
import cv2

# Function to crop the image using Pillow
def crop_image_pillow(image, top, bottom, left, right):
    width, height = image.size
    left_px = int(width * left)
    top_px = int(height * top)
    right_px = int(width * (1 - right))
    bottom_px = int(height * (1 - bottom))
    return image.crop((left_px, top_px, right_px, bottom_px))

# Main Streamlit app
def main():
    st.title("Billets Counting Application")
    
    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        st.subheader("Original Image")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Crop the Image Section
        st.subheader("Crop the Image")
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write("### Cropping Controls")
            top = st.slider("Top Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            bottom = st.slider("Bottom Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            left = st.slider("Left Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            right = st.slider("Right Crop (%)", 0.0, 0.5, 0.0, step=0.01)
            cropped_image = crop_image_pillow(image, top, bottom, left, right)
            st.image(cropped_image, caption="Cropped Image", use_column_width=True)

        # Reference Circle Section
        st.subheader("Reference Circle Selection")
        with col1:
            st.write("### Reference Circle Controls")
            ref_top = st.slider("Ref. Top Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_bottom = st.slider("Ref. Bottom Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_left = st.slider("Ref. Left Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_right = st.slider("Ref. Right Position (%)", 0.0, 1.0, 0.25, step=0.01)
            ref_circle = crop_image_pillow(cropped_image, ref_top, ref_bottom, ref_left, ref_right)
            st.image(ref_circle, caption="Selected Reference Circle", use_column_width=True)

        # Radius Calculation and Cylinder Detection
        radius = (ref_circle.size[0] + ref_circle.size[1]) // 4
        st.write(f"Estimated Radius: {radius} pixels")

        # Detect Cylinders
        st.subheader("Detect Billets")
        if st.button("Detect"):
            cropped_image_np = np.array(cropped_image)  # Convert PIL to NumPy array
            gray = cv2.cvtColor(cropped_image_np, cv2.COLOR_BGR2GRAY)
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
                    cv2.circle(cropped_image_np, (x, y), r, (0, 255, 0), 2)

                st.image(cropped_image_np, caption="Billets Cylinders", use_column_width=True)
                st.success(f"Number of Billets Detected: {len(circles)}")
            else:
                st.warning("No Billets Detected")

# Run the Streamlit app
if __name__ == "__main__":
    main()
