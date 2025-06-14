# 🛡️ Hiding Text Inside an Image using Layered Steganography

---

This project implements a **layered steganography system** to securely hide text messages inside lossless images (PNG) using:  
✅ **XOR encryption**  

✅ **AES encryption**

✅ **zlib compression** 

✅ **Least Significant Bit (LSB) embedding at random positions**

Built using **Python**, **Streamlit**, and visualized with **Graphviz**.

---

## 🚀 Features

- 🔒 Dual-layer encryption (XOR + AES) for enhanced security
   
- ⚡ Compression to optimize hidden payload size
   
- 🖼️ LSB-based embedding with random positions to minimize detectability
  
- 🌈 Interactive Streamlit web app with gradient UI
    
- 📈 Auto-generated algorithm flowchart using Graphviz  

---

## 🛠️ Technologies Used

- Python 3.x
  
- PyCryptodome (AES encryption)
  
- zlib (compression)
  
- Streamlit (web UI)
  
- Graphviz (flowchart generation)
   
- NumPy, Pillow  

---

## 📂 Project Structure

├── app.py # Streamlit app code

├── example_image.png # Example lossless image

├── README.md # Project documentation

---

## 📌 How It Works

1️⃣ XOR encrypt the input text using a key

2️⃣ AES encrypt the XOR ciphertext with a second key

3️⃣ Compress the AES ciphertext

4️⃣ Embed the compressed bits into LSBs of image pixels at random positions

5️⃣ To decode: Extract → decompress → AES decrypt → XOR decrypt

---

## ⚙️ How to Run

### 1️⃣ Clone the repository

### 2️⃣ Install dependencies

### 3️⃣ Run the app

---

## 📝 Future Scope

- Adaptive LSB based on image features (edges/textures)

- Multi-channel (RGB) embedding

- Error correction codes for added robustness

- Video/audio steganography support

  ---

  ## 🤝 License

This project is licensed under the MIT License.  
See the LICENSE file (LICENSE) for details.


