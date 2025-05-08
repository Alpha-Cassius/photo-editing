# 🎨 Lovable Edits — AI-Powered Image Editing in Streamlit

**Lovable Edits** is a feature-rich, interactive photo editing web app built using **Streamlit**, **Pillow**, **OpenCV**, **rembg**, and **pilgram2**. It offers a broad suite of tools—from basic adjustments to advanced AI-powered effects like background removal and Instagram-style filters—allowing users to create stunning images with ease.

---

## 🚀 Features

🔧 **Basic Edits**

* Rotate, flip, crop, and resize your image
* Adjust brightness, contrast, sharpness, and color

🎨 **Artistic Filters**

* Apply 40+ **Instagram-inspired filters** using `pilgram2`
* AI-based **art effects**: Sketch, Cartoon, Charcoal

🪄 **Background Editing**

* One-click **background removal** using `rembg`
* Replace background with an image or solid color

🖼️ **Overlays & Blending**

* Add and position custom overlays
* Soft-light image blending with adjustable opacity

🧩 **Stickers**

* Upload your own stickers (PNG/JPG) to a folder and use them in-app
* Resize and reposition stickers dynamically

🔤 **Text Tools**

* Add multiple text layers with:

  * Custom font support
  * Font size and color
  * Bold, italic, underline
  * Precise X/Y positioning

📥 **Downloadable Output**

* Preview final result
* Download edited image as PNG

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lovable-edits.git
cd lovable-edits
```

### 2. Install Dependencies

Make sure Python 3.8+ is installed, then install required packages:

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install manually:

```bash
pip install streamlit pillow numpy opencv-python-headless rembg pilgram2
```

### 3. Prepare Assets

Create the necessary folders under the root directory:

```bash
mkdir -p DATABASE/STICKERS
mkdir -p DATABASE/FONTS
```

* Add your PNG/JPG stickers to `DATABASE/STICKERS`
* Add your `.ttf` or `.otf` font files to `DATABASE/FONTS`

---

## ▶️ Running the App

Launch the Streamlit server with:

```bash
streamlit run photoshop.py
```

Then open your browser to [http://localhost:8501](http://localhost:8501).

---

## 📂 Project Structure

```
lovable-edits/
├── .streamlit
│   └── config.toml
├── photoshop.py               # Main Streamlit app
├── DATABASE/
│   ├── STICKERS/              # Custom sticker images
│   └── FONTS/                 # Custom fonts
└── requirements.txt
```

---

## 🧠 How It Works

### Core Technologies:

* **Streamlit** – for building the interactive frontend
* **Pillow (PIL)** – image manipulation (rotation, filters, drawing)
* **OpenCV** – sketch, cartoon, and charcoal AI effects
* **rembg** – seamless background removal using deep learning
* **pilgram2** – high-quality Instagram-like photo filters
* **NumPy** – blending and image transformations

### Session Management

The app uses `st.session_state` to manage overlays, stickers, and text layers—allowing for persistent edits across UI interactions.

---

## 🧪 Supported Filters & Styles

### Instagram Filters (via `pilgram2`)

Examples:

* `clarendon`, `gingham`, `hefe`, `juno`, `lark`, `lofi`, `moon`, `nashville`, etc.

### Art Effects (via OpenCV)

* `Sketch`: Pencil sketch with edge detection
* `Cartoon`: Stylized bilateral filter and adaptive threshold
* `Charcoal`: Edge-based grayscale stylization

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📬 Contact

Made with ❤️ by Vaibhav Pandey.

