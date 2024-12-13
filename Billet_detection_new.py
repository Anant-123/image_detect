import cv2
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image


def detect_bars(image, avg_radius):
    """Detect cylindrical bars based on reference circle radius."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=avg_radius * 1.5,
        param1=50, param2=30, minRadius=int(avg_radius * 0.8), maxRadius=int(avg_radius * 1.2)
    )

    count = 0
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        count = len(circles)
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(image, (x - r, y - r), (x + r, y + r), (0, 128, 255), 2)
    return image, count


def main():
    st.title("Cylinder Detection in Images")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Load and display the image
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.subheader("Step 1: Crop Region of Interest (ROI)")
        st.write("Use the box tool below to draw a rectangle around the ROI.")

        # Drawable canvas for cropping
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Transparent red
            stroke_width=2,
            stroke_color="#FF0000",
            background_image=image,
            update_streamlit=True,
            height=image_np.shape[0],
            width=image_np.shape[1],
            drawing_mode="rect",
            key="crop_canvas",
        )

        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            if len(objects) > 0:
                # Extract cropping coordinates
                obj = objects[0]  # Get the first drawn rectangle
                left = int(obj["left"])
                top = int(obj["top"])
                width = int(obj["width"])
                height = int(obj["height"])
                roi_image = image_np[top : top + height, left : left + width]

                # Display the cropped ROI
                st.image(roi_image, caption="Cropped ROI", use_column_width=True)
                st.session_state["roi_image"] = roi_image

        # Step 2: Select Reference Circles
        if "roi_image" in st.session_state:
            st.subheader("Step 2: Select Reference Circles")
            circle_radii = []
            for i in range(2):
                st.write(f"Select dimensions for Reference Circle {i+1}")
                w = st.slider(f"Width for Circle {i+1}", 1, 100, 50)
                h = st.slider(f"Height for Circle {i+1}", 1, 100, 50)
                radius = (w + h) // 4
                circle_radii.append(radius)
            if len(circle_radii) == 2:
                avg_radius = sum(circle_radii) // len(circle_radii)
                st.success(f"Average radius of selected circles: {avg_radius}")
                st.session_state["avg_radius"] = avg_radius

        # Step 3: Detect Cylinders
        if "roi_image" in st.session_state and "avg_radius" in st.session_state:
            st.subheader("Step 3: Detect Cylindrical Bars")
            detect_button = st.button("Detect Cylinders")
            if detect_button:
                roi_image = st.session_state["roi_image"]
                avg_radius = st.session_state["avg_radius"]
                output_image, bar_count = detect_bars(roi_image, avg_radius)
                st.image(output_image, channels="BGR", caption="Detected Bars", use_column_width=True)
                st.success(f"Number of cylinders detected: {bar_count}")


if __name__ == "__main__":
    main()
