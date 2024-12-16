import streamlit as st
from PIL import Image


def crop_image_with_pillow(image, top_left, bottom_right):
    """
    Crop an image using Pillow.
    Parameters:
    - image: PIL Image object
    - top_left: (x1, y1) coordinates of the top-left corner
    - bottom_right: (x2, y2) coordinates of the bottom-right corner
    Returns:
    - Cropped image as a PIL Image object
    """
    return image.crop((*top_left, *bottom_right))


def main():
    st.title("Image Cropping with 4-Point Selection")
    
    # Upload the image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Load the uploaded image using PIL
        image = Image.open(uploaded_file)
        st.subheader("Uploaded Image")
        st.image(image, caption="Original Image", use_column_width=True)

        # Image dimensions
        width, height = image.size
        st.write(f"Image Dimensions: Width = {width}, Height = {height}")
        
        st.subheader("Define Crop Area (Coordinates)")

        # Input fields for the crop area
        col1, col2 = st.columns(2)
        with col1:
            x1 = st.number_input("Top-left X (x1)", min_value=0, max_value=width, value=0)
            y1 = st.number_input("Top-left Y (y1)", min_value=0, max_value=height, value=0)
        with col2:
            x2 = st.number_input("Bottom-right X (x2)", min_value=0, max_value=width, value=width)
            y2 = st.number_input("Bottom-right Y (y2)", min_value=0, max_value=height, value=height)

        # Crop button
        if st.button("Crop Image"):
            # Validate crop coordinates
            if x1 < x2 and y1 < y2:
                cropped_image = crop_image_with_pillow(image, (x1, y1), (x2, y2))
                st.subheader("Cropped Image")
                st.image(cropped_image, caption="Cropped Image", use_column_width=True)
            else:
                st.error("Invalid coordinates! Ensure x1 < x2 and y1 < y2.")

        st.write("Adjust the coordinates using the input fields above to crop your image.")


if __name__ == "__main__":
    main()
