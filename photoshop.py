import io
import os
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFont, ImageDraw
from rembg import remove
import pilgram2 as pilgram
import cv2

# --- Constants ---
INSTAGRAM_FILTERS = [
    "None", "_1977", "aden", "ashby", "amaro", "brannan", "brooklyn", "charmes",
    "clarendon", "crema", "dogpatch", "earlybird", "gingham", "ginza", "hefe",
    "helena", "hudson", "inkwell", "juno", "kelvin", "lark", "lofi", "ludwig",
    "maven", "mayfair", "moon", "nashville", "perpetua", "poprocket", "reyes",
    "rise", "sierra", "skyline", "slumber", "stinson", "sutro", "toaster",
    "valencia", "walden", "willow", "xpro2"
]

STICKER_DIR = "DATABASE/STICKERS"
PRIMARY_COLOR = "#4BFFD4"
FONT_DIR = "DATABASE/FONTS"

# --- Helper Functions ---
def load_image(path):
    try:
        return Image.open(path)
    except Exception:
        return None

def get_sticker_files():
    return [os.path.join(STICKER_DIR, f) for f in os.listdir(STICKER_DIR)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))]

def pil_to_cv(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2RGB)

def cv_to_pil(cv_img):
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGBA))

def soft_light(base_np, overlay_np, opacity=0.5):
    return base_np * (1 - opacity) + overlay_np * opacity

def download_image(img, filename="edited_image.png"):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()

def get_font_files():
    return [f for f in os.listdir(FONT_DIR) if f.lower().endswith((".ttf", ".otf"))]

def load_font(font_name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, font_name), size)
    except Exception as e:
        print(f"Error loading font {font_name}: {e}") # Important for debugging
        return None

# --- App Setup ---
st.set_page_config(page_title="Lovable Edits", layout="wide")
st.title("🎨 Lovable Edits")

if "stickers" not in st.session_state:
    st.session_state.stickers = []  # List of dicts: {path, x, y, width, height}

if "texts" not in st.session_state:
    st.session_state.texts = []  # List of dicts

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    original_image = Image.open(uploaded_file).convert("RGBA")
    edited_image = original_image.copy()
    img_width, img_height = edited_image.size

    with st.sidebar:
        st.header("Basic Edits")
        rotate_angle = st.slider("Rotate", -180, 180, 0)
        flip_horizontal = st.checkbox("Flip Horizontal")
        flip_vertical = st.checkbox("Flip Vertical")

        st.header("Crop")
        crop_enabled = st.checkbox("Enable Crop")
        crop_left = st.slider("Left", 0, img_width, 0) if crop_enabled else 0
        crop_right = st.slider("Right", 0, img_width, img_width) if crop_enabled else img_width
        crop_top = st.slider("Top", 0, img_height, 0) if crop_enabled else img_height
        crop_bottom = st.slider("Bottom", 0, img_height, img_height) if crop_enabled else img_height

        st.header("Resize")
        resize_enabled = st.checkbox("Enable Resize")
        new_width = st.slider("Width", 50, img_width * 2, img_width) if resize_enabled else img_width
        new_height = st.slider("Height", 50, img_height * 2, img_height) if resize_enabled else img_height
        maintain_aspect_ratio = st.checkbox("Maintain Aspect Ratio", True)

        st.header("Adjustments")
        brightness = st.slider("Brightness", 0.1, 3.0, 1.0)
        contrast = st.slider("Contrast", 0.1, 3.0, 1.0)
        sharpness = st.slider("Sharpness", 1.0, 3.0, 1.0)
        color_adjustment = st.slider("Color", 0.0, 2.0, 1.0)

        st.header("Filters")
        filter_name = st.selectbox("Instagram-like Filters", INSTAGRAM_FILTERS)

        st.header("Art Effects")
        art_effect = st.selectbox("Style", ["None", "Sketch", "Cartoon", "Charcoal"])

        st.header("Background")
        remove_bg = st.checkbox("Remove Background")
        bg_replace = st.file_uploader("Replace Background", type=["jpg", "png"])
        bg_color = st.color_picker("Background Color", "#ffffff")

        st.header("Blending")
        blend_img_file = st.file_uploader("Upload Image to Blend", type=["jpg", "jpeg", "png"])
        blend_opacity = st.slider("Opacity", 0.0, 1.0, 0.5)

        st.header("Add Overlay")
        uploaded_overlay = st.file_uploader("Upload PNG Overlay", type=["png"])
        if uploaded_overlay:
            overlay_image = Image.open(uploaded_overlay).convert("RGBA")
            overlay_width, overlay_height = overlay_image.size
            st.session_state.overlay_data = {
                "image": overlay_image,
                "x": 50,
                "y": 50,
                "width": overlay_width,
                "height": overlay_height
            }
            with st.expander("⚙️ Edit Overlay"):
                overlay = st.session_state.overlay_data
                col1, col2 = st.columns(2)
                with col1:
                    overlay["x"] = st.slider("Overlay X Position", 0, edited_image.size[0], overlay["x"])
                    overlay["y"] = st.slider("Overlay Y Position", 0, edited_image.size[1], overlay["y"])
                with col2:
                    overlay["width"] = st.slider("Overlay Width", 20, edited_image.size[0], overlay["width"])
                    overlay["height"] = st.slider("Overlay Height", 20, edited_image.size[1], overlay["height"])
        else:
            st.session_state.overlay_data = None

    # --- Apply Basic Edits ---
    if rotate_angle != 0:
        edited_image = edited_image.rotate(rotate_angle, expand=True)
    if flip_horizontal:
        edited_image = ImageOps.mirror(edited_image)
    if flip_vertical:
        edited_image = ImageOps.flip(edited_image)

    if crop_enabled:
        edited_image = edited_image.crop((crop_left, crop_top, crop_right, crop_bottom))

    if resize_enabled:
        if maintain_aspect_ratio:
            aspect_ratio = img_width / img_height
            if new_width / new_height > aspect_ratio:
                new_width = int(new_height * aspect_ratio)
            else:
                new_height = int(new_width / aspect_ratio)
        edited_image = edited_image.resize((new_width, new_height))

    edited_image = ImageEnhance.Brightness(edited_image).enhance(brightness)
    edited_image = ImageEnhance.Contrast(edited_image).enhance(contrast)
    edited_image = ImageEnhance.Sharpness(edited_image).enhance(sharpness)
    edited_image = ImageEnhance.Color(edited_image).enhance(color_adjustment)

    # --- Filter ---
    if filter_name != "None":
        try:
            edited_image = getattr(pilgram, filter_name)(edited_image)
        except AttributeError:
            st.warning(f"Filter '{filter_name}' not supported.")

    # --- Art Effects ---
    if art_effect == "Sketch":
        gray = cv2.cvtColor(pil_to_cv(edited_image), cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        edited_image = Image.fromarray(sketch).convert("RGBA")
    elif art_effect == "Cartoon":
        img = pil_to_cv(edited_image)
        gray = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        edited_image = cv_to_pil(cartoon)
    elif art_effect == "Charcoal":
        img = pil_to_cv(edited_image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(blur, 100, 200)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        edited_image = cv_to_pil(edges)

    # --- Background ---
    if remove_bg:
        img_bytes = io.BytesIO()
        edited_image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        edited_image = Image.open(io.BytesIO(remove(img_bytes))).convert("RGBA")

    if bg_replace:
        bg = Image.open(bg_replace).resize(edited_image.size).convert("RGBA")
        # Ensure both images have the same mode before pasting.
        if edited_image.mode != bg.mode:
            bg = bg.convert(edited_image.mode)  # change the mode of the background
        bg.paste(edited_image, (0, 0), edited_image)
        edited_image = bg
    elif bg_color:
        background = Image.new("RGBA", edited_image.size, bg_color)
        # Ensure both images have the same mode before pasting.
        if edited_image.mode != background.mode:
            background = background.convert(edited_image.mode)  # change the mode of the background
        if edited_image.mode != 'RGBA':
            edited_image = edited_image.convert('RGBA')
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        background.paste(edited_image, (0, 0), edited_image)
        edited_image = background

    # --- Blending ---
    if blend_img_file:
        blend_img = Image.open(blend_img_file).resize(edited_image.size).convert("RGBA")
        base_np = np.asarray(edited_image).astype(float)
        overlay_np = np.asarray(blend_img).astype(float)
        blended = soft_light(base_np, overlay_np, blend_opacity)
        edited_image = Image.fromarray(np.uint8(blended.clip(0, 255)))

    # --- Paste Overlay ---
    if st.session_state.overlay_data:
        overlay = st.session_state.overlay_data
        resized_overlay = overlay["image"].resize((overlay["width"], overlay["height"]))
        edited_image.paste(resized_overlay, (overlay["x"], overlay["y"]), resized_overlay)

    # --- Sticker UI ---
    with st.expander("🧩 Add Stickers"):
        sticker_files = get_sticker_files()
        if not sticker_files:
            st.info("No stickers found in the folder.")
        else:
            for i in range(0, len(sticker_files), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(sticker_files):
                        file = sticker_files[idx]
                        img = load_image(file)
                        with col:
                            with st.container():
                                if img:
                                    st.image(img.resize((120, 120)))
                                    if st.button("Add Sticker ➕ ", key=f"add_{idx}"):
                                        st.session_state.stickers.append({
                                            "path": file,
                                            "x": 50,
                                            "y": 50,
                                            "width": 100,
                                            "height": 100
                                        })

    # --- Edit Stickers ---
    if st.session_state.stickers:
        with st.expander("✏️ Edit Stickers"):
            for i, sticker in enumerate(st.session_state.stickers):
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.stickers[i]["x"] = st.slider(
                        f"X Position {i+1}", 0, edited_image.size[0], sticker["x"], key=f"x_{i}")
                    st.session_state.stickers[i]["y"] = st.slider(
                        f"Y Position {i+1}", 0, edited_image.size[1], sticker["y"], key=f"y_{i}")
                with col2:
                    st.session_state.stickers[i]["width"] = st.slider(
                        f"Width {i+1}", 20, 300, sticker["width"], key=f"w_{i}")
                    st.session_state.stickers[i]["height"] = st.slider(
                        f"Height {i+1}", 20, 300, sticker["height"], key=f"h_{i}")

    # --- Edit Text ---
    with st.expander("🔤 Add/Edit Text"):
        if st.button("Add New Text"):
            st.session_state.texts.append({
                "text": "Your Text",
                "x": 50,
                "y": 50,
                "font": get_font_files()[0] if get_font_files() else None,
                "size": 32,
                "color": "#000000",
                "bold": False,
                "italic": False,
                "underline": False,
            })

        for i, txt in enumerate(st.session_state.texts):
            st.markdown(f"**Text #{i+1}**")
            txt["text"] = st.text_input("Text", txt["text"], key=f"text_{i}")
            txt["x"] = st.slider("X Position", 0, edited_image.size[0], txt["x"], key=f"tx_{i}")
            txt["y"] = st.slider("Y Position", 0, edited_image.size[1], txt["y"], key=f"ty_{i}")
            txt["size"] = st.slider("Font Size", 10, 150, txt["size"], key=f"size_{i}")
            txt["color"] = st.color_picker("Text Color", txt["color"], key=f"color_{i}")
            txt["font"] = st.selectbox("Font", get_font_files(), index=get_font_files().index(txt["font"]) if txt["font"] in get_font_files() else 0, key=f"font_{i}")
            col1, col2, col3 = st.columns(3)
            with col1:
                txt["bold"] = st.checkbox("Bold", txt["bold"], key=f"bold_{i}")
            with col2:
                txt["italic"] = st.checkbox("Italic", txt["italic"], key=f"italic_{i}")
            with col3:
                txt["underline"] = st.checkbox("Underline", txt["underline"], key=f"underline_{i}")

    # --- Paste Stickers ---
    for sticker_data in st.session_state.stickers:
        sticker_img = load_image(sticker_data["path"])
        if sticker_img:
            sticker = sticker_img.resize((sticker_data["width"], sticker_data["height"]))
            edited_image.paste(sticker, (sticker_data["x"], sticker_data["y"]), sticker)

    # --- Draw Text on Image ---
    draw = ImageDraw.Draw(edited_image)
    for txt in st.session_state.texts:
        try:
            font_style = load_font(txt["font"], txt["size"])
            if font_style: # only draw if the font loaded successfully
                draw.text((txt["x"], txt["y"]), txt["text"], font=font_style, fill=txt["color"])
                # Underline: simple hack — draw a line under text
                if txt["underline"]:
                    text_width, text_height = draw.textsize(txt["text"], font=font_style)
                    draw.line(
                        [(txt["x"], txt["y"] + text_height + 2), (txt["x"] + text_width, txt["y"] + text_height + 2)],
                        fill=txt["color"], width=2
                    )
        except Exception as e:
             print(f"Error drawing text: {e}")

    st.image(edited_image, caption="Final Image", use_container_width=True)

    # --- Text Area for AI ---
    #ai_prompt = st.text_area("Describe the changes you want using AI:", "")

    # --- Download Button ---
    download_bytes = download_image(edited_image)
    st.download_button(
        label="Download Image",
        data=download_bytes,
        file_name="edited_image.png",
        mime="image/png"
    )
