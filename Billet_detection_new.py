import streamlit as st
from PIL import Image
import numpy as np


def crop_image_with_coords(image, x1, y1, x2, y2):
    """
    Crop an image using the provided coordinates.
    Parameters:
    - image: NumPy array of the image
    - x1, y1: Top-left corner coordinates
    - x2, y2: Bottom-right corner coordinates
    """
    return image[y1:y2, x1:x2]


def main():
    st.title("Image Cropping Application Using 4 Corners")

    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        image_np = np.array(image)  # Convert PIL image to NumPy array for processing

        # Display the original image
        st.subheader("Original Image")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Get image dimensions
        height, width = image_np.shape[:2]

        st.subheader("Select 4 Corners for Cropping")

        # Inputs for top-left and bottom-right corners
        x1 = st.number_input("X1 (Top-left corner)", min_value=0, max_value=width, value=0)
        y1 = st.number_input("Y1 (Top-left corner)", min_value=0, max_value=height, value=0)
        x2 = st.number_input("X2 (Bottom-right corner)", min_value=0, max_value=width, value=width)
        y2 = st.number_input("Y2 (Bottom-right corner)", min_value=0, max_value=height, value=height)

        # Crop and display the image when the button is clicked
        if st.button("Crop Image"):
            # Ensure valid coordinates
            if x1 < x2 and y1 < y2:
                cropped_image = crop_image_with_coords(image_np, int(x1), int(y1), int(x2), int(y2))
                st.subheader("Cropped Image")
                st.image(cropped_image, caption="Cropped Image", use_column_width=True)
            else:
                st.error("Invalid coordinates: Make sure X1 < X2 and Y1 < Y2.")

        st.write("Adjust the coordinates using the inputs above to crop your image.")


if __name__ == "__main__":
    main()
