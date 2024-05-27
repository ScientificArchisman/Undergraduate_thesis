import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import cv2
from io import BytesIO
plt.style.use(["science", "notebook", "grid", "dark_background"])

# img = plt.imread("/Users/archismanchakraborti/Desktop/python files/Dissertation/images/most-colorful-birds-on-the-planet.jpg")


def show_img(img:np.ndarray) -> None:
    """ Show image 
    Args:
        img: image to show
    Returns:
        None"""
    plt.figure(figsize=(10,10))
    plt.axis("off")
    plt.imshow(img)
    plt.show()

def get_channels(img:np.ndarray) -> np.ndarray:
    """ Get channels from image
    Args:
        img: image to get channels from
    Returns:
        red, green, blue: channels from image"""
    red, green, blue = img[:,:,0], img[:,:,1], img[:,:,2]
    zero_arr = np.zeros_like(red)
    red = np.stack([red, zero_arr, zero_arr], axis=2)
    green = np.stack([zero_arr, green, zero_arr], axis=2)
    blue = np.stack([zero_arr, zero_arr, blue], axis=2)
    return red, green, blue

def plot_channels(img:np.ndarray) -> None:
    """ Plot channels from image
    Args:
        img: image to plot channels from
    Returns:
        None"""
    red, green, blue = get_channels(img)
    fig, ax = plt.subplots(1, 3, figsize=(20, 10))
    for axi in ax.ravel():
        axi.axis("off")
    ax[0].imshow(red, cmap="Reds")
    ax[0].set_title("Red")
    ax[1].imshow(green, cmap = "Greens")
    ax[1].set_title("Green")
    ax[2].imshow(blue, cmap = "Blues")
    ax[2].set_title("Blue")

def get_bar(img):
    red_color = cv2.calcHist([img], [0], None, [256], [0, 256])
    green_color = cv2.calcHist([img], [1], None, [256], [0, 256])
    blue_color = cv2.calcHist([img], [2], None, [256], [0, 256])
    return red_color, green_color, blue_color



st.set_page_config(page_title="RGB Channels \n Archisman Chakraborti", 
                   page_icon=":rainbow:", layout="wide")

st.sidebar.header("Please Filter Here:")




file = st.file_uploader("Please choose a file", type = ["jpg", "png", "jpeg"])
show_file = st.empty()

if not file:
    show_file.info("Please upload a file of type: " + ", ".join(["jpg", "png", "jpeg"]))
    st.stop()

if isinstance(file, BytesIO):
    # file = BytesIO(file.read())
    img = plt.imread(file)
    # st.image(img, use_column_width=True, clamp=True, channels="RGB",
    #             caption="Original Image", output_format="auto")

    
   

channel = st.sidebar.multiselect(
    "Select the Mode:",
    options=["Red", "Green", "Blue", "All", "Histograms"],
    default=["All"]
)

st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the Type:",
    options=["Image", "Video"],
    default=["Image"]
)


# ---- MAINPAGE ----
st.title(":low_brightness: RGB Channels :low_brightness:")
st.markdown("#")

red, green, blue = get_channels(img)

st.markdown("---")

if "All" in channel:
    left_col, mid_col, right_col = st.columns(3)
    with left_col:
        st.header("Red")
        st.image(red, use_column_width=True, clamp=True, channels="RGB",
             caption="Red Channel", output_format="auto")

    with mid_col:
        st.header("Green")
        st.image(green, use_column_width=True, clamp=True, channels="RGB",
             caption="Green Channel", output_format="auto")
    
    with right_col:
        st.header("Blue")
        st.image(blue, use_column_width=True, clamp=True, channels="RGB",
             caption="Blue Channel", output_format="auto")

if "Red" in channel:
    left_col,  right_col = st.columns(2)
    with left_col:
        st.header("Red")
        st.image(red, use_column_width=True, clamp=True, channels="RGB",
             caption="Red Channel", output_format="auto")
    with right_col:
        st.image(img, use_column_width=True, clamp=True, channels="RGB", 
               caption="Original Image", output_format="auto")

    
if "Green" in channel:
    left_col, right_col = st.columns(2)
    with left_col:
        st.header("Green")
        st.image(green, use_column_width=True, clamp=True, channels="RGB",
             caption="Green Channel", output_format="auto")
    with right_col:
        st.image(img, use_column_width=True, clamp=True, channels="RGB", 
               caption="Original Image", output_format="auto")
        
if "Blue" in channel:
    left_col, right_col = st.columns(2)
    with left_col:
        st.header("Blue")
        st.image(blue, use_column_width=True, clamp=True, channels="RGB",
             caption="Blue Channel", output_format="auto")
    with right_col:
        st.image(img, use_column_width=True, clamp=True, channels="RGB", 
               caption="Original Image", output_format="auto")

if "Histograms" in channel:
    st.header("Histograms")
    red_color, green_color, blue_color = get_bar(img)
    fig, ax = plt.subplots(1, 3, figsize=(20, 8))
    ax[0].hist(red_color, color = "tomato", bins=25, label="Red", 
                alpha=0.5)
    ax[0].set_title("Red")
    ax[1].hist(green_color, color = "g", bins=25, label="Green",
                alpha=0.6, histtype="stepfilled", ec="k", lw=1)
    ax[1].set_title("Green")
    ax[2].hist(blue_color, color = "cyan", bins=25, label="Blue",
                alpha=0.6, histtype="stepfilled", ec="k", lw=1)
    ax[2].set_title("Blue")
    for axi in ax.ravel():
        axi.legend()
        axi.set_xlabel("Bins")
        axi.set_ylabel("No. of Pixels")
    st.pyplot(fig)
