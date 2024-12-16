import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2


# Main Streamlit app
def main():
    st.title("Billets Counting Application with Interactive Cropping")
    
    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        image_np = np.array(image)  # Convert to NumPy array

        # Original Image Display
        st.subheader("Original Image")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Interactive Cropping Section
        st.subheader("Interactive Cropping Tool")

        # Set up the canvas for cropping
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Transparent orange
            stroke_width=2,
            stroke_color="blue",
            background_image=image,
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode="rect",  # Rectangle tool
            key="crop_canvas",
        )

        # Process the cropped area
        if canvas_result.json_data is not None:
            for shape in canvas_result.json_data["objects"]:
                if shape["type"] == "rect":
                    # Get the bounding box of the rectangle
                    left = int(shape["left"])
                    top = int(shape["top"])
                    width = int(shape["width"])
                    height = int(shape["height"])

                    # Crop the image using the bounding box
                    cropped_image = image_np[top : top + height, left : left + width]

                    # Display cropped image
                    st.subheader("Cropped Image")
                    st.image(cropped_image, caption="Cropped Area", use_column_width=True)

                    # Add Reference Circle Cropping Section
                    st.subheader("Select Reference Circle")
                    st.info("Draw another rectangle around the reference circle using the cropping tool.")

        # Radius Calculation and Cylinder Detection
        if st.button("Detect Billets"):
            try:
                gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (11, 11), 0)

                # Estimate radius based on the cropped area
                estimated_radius = min(cropped_image.shape[:2]) // 4
                st.write(f"Estimated Radius: {estimated_radius} pixels")

                # Detect cylinders
                circles = cv2.HoughCircles(
                    blurred,
                    cv2.HOUGH_GRADIENT,
                    dp=1.2,
                    minDist=estimated_radius * 1.5,
                    param1=50,
                    param2=30,
                    minRadius=int(estimated_radius * 0.8),
                    maxRadius=int(estimated_radius * 1.2),
                )

                if circles is not None:
                    circles = np.round(circles[0, :]).astype("int")
                    for (x, y, r) in circles:
                        cv2.circle(cropped_image, (x, y), r, (0, 255, 0), 2)

                    st.image(cropped_image, caption="Billets Detected", use_column_width=True)
                    st.success(f"Number of Billets Detected: {len(circles)}")
                else:
                    st.warning("No Billets Detected.")
            except NameError:
                st.error("Please crop the image first before detecting billets.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
