import numpy as np
import matplotlib.pyplot as plt
import streamlit as st  # pip install streamlit
from io import BytesIO


def conv2d(X: np.ndarray, K: np.ndarray) -> np.ndarray:
    """2D convolution
    Args:
        X (np.ndarray): input array
        K (np.ndarray): kernel array
    Returns:
        np.ndarray: output array"""
    h, w = K.shape # kernel size
    Y = np.zeros((X.shape[0]-h+1, X.shape[1]-w+1)) # output size
    for i in range(Y.shape[0]): # loop over output
        for j in range(Y.shape[1]): # loop over output
            Y[i, j] = (X[i:i+h, j:j+w] * K).sum() # element-wise multiplication and sum
    return Y


kernels = {
    "sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
    "Ridge" : np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]]),
    "edge": np.array([[1, 0, -1], [0, 0, 0], [-1, 0, 1]]),
    "emboss": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]),
    "blur": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])/9 ,
}

# ------------------>Streamlit<----------------------
st.set_page_config(page_title="Convolution \n Archisman Chakraborti", 
                   page_icon=":rainbow:", layout="wide")


# ------------------>File selection<----------------------
file = st.sidebar.file_uploader("Please choose a file", type = ["jpg", "png", "jpeg"],
                        label_visibility="collapsed")
show_file = st.empty()
if not file:
    show_file.info("Please upload a file of type: " + ", ".join(["jpg", "png", "jpeg"]))
    st.stop()
if isinstance(file, BytesIO):
    img = plt.imread(file)

# ------------------>Kernel and image selection<----------------------
kernel = st.sidebar.radio("Select the Kernel", tuple(kernels.keys()), index=0, 
                  help="This is a 3x3 kernel")
channel = st.sidebar.multiselect("Select the channel", ["Red", "Green", "Blue", 
                                                        "Original"],help="Select the channel to be displayed")

# ------------------>Convolution<----------------------
red, green, blue = img[:,:,0], img[:,:,1], img[:,:,2]
zero_arr = np.zeros_like(red)
red_stacked = np.stack([red, zero_arr, zero_arr], axis=2)
green_stacked = np.stack([zero_arr, green, zero_arr], axis=2)
blue_stacked = np.stack([zero_arr, zero_arr, blue], axis=2)
# red_conv = conv2d(red, kernels[kernel])
# green_conv = conv2d(green, kernels[kernel])
# blue_conv = conv2d(blue, kernels[kernel])



# ------------------>Streamlit<----------------------
type = st.selectbox("Please choose a type", ["Kernel", "Pictures", "None"], 2)

if type == "None":
    st.title("Please choose a type")
    
if type == "Kernel":
    st.title("Kernels")

    st.dataframe(kernels[kernel], width=2000, height=2000)


if type == "Pictures":
    st.title("Pictures")

    if "Red" in channel:
        left_col, right_col = st.columns(2)
        with left_col:
            st.header("Red image")
            fig, ax = plt.subplots(1, figsize=(20, 8))
            ax.imshow(red, cmap="Reds")
            ax.axis("off")
            st.pyplot(fig)

        with right_col:
            st.header("Red image after convolution")
            fig, ax = plt.subplots(1, figsize=(20, 8))
            ax.imshow(conv2d(red, kernels[kernel]), cmap="gray", 
                      vmin=0, vmax=255
                       )
            ax.axis("off")
            st.pyplot(fig)
            
    if "Green" in channel:
        left_col, right_col = st.columns(2)
        with left_col:
            st.header("Green image")
            fig, ax = plt.subplots(1, figsize=(20, 8))
            ax.imshow(green, cmap="Greens")
            ax.axis("off")
            st.pyplot(fig)

        with right_col:
            st.header("Green image after convolution")
            fig, ax = plt.subplots(1, figsize=(20, 8))
            ax.imshow(conv2d(green, kernels[kernel]), cmap="gray",
                        vmin=0, vmax=255
                        )
            ax.axis("off")
            st.pyplot(fig)
            
            
    
    if "Blue" in channel:
        left_col, right_col = st.columns(2)
        with left_col:
            st.header("Blue image")
            fig, ax = plt.subplots(1, figsize=(20, 8))
            ax.imshow(blue, cmap="Blues")
            ax.axis("off")
            st.pyplot(fig)

        with right_col:
            st.header("Blue image after convolution")
            fig, ax = plt.subplots(1, figsize=(20, 8))
            ax.imshow(conv2d(blue, kernels[kernel]), cmap="gray", 
                      vmin=0, vmax=255
                       )
            ax.axis("off")
            st.pyplot(fig)

            # st.image(conv2d(blue, kernels[kernel]), use_column_width=True, clamp=True,
            #             caption="Blue channel of the image after convolution")
                     
    if "Original" in channel:
        left_col, right_col = st.columns(2)
        with left_col:
            st.header("Original image")
            st.image(img, use_column_width=True, clamp=True,
                    caption="Original image")
        with right_col:
            st.header("Original image after convolution")
            red_part = conv2d(red, kernels[kernel])
            green_part = conv2d(green, kernels[kernel])
            blue_part = conv2d(blue, kernels[kernel])
            img_conv = np.stack([red_part, green_part, blue_part], axis=2)
            st.image(img_conv, use_column_width=True, clamp=True,
                     caption="Original image after convolution",
                        channels="RGB")
            
            
        
