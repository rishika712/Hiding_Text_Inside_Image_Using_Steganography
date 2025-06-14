import streamlit as st
from PIL import Image
import numpy as np
import zlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import random
import io

# 🌈 Apply gradient background using CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #74ebd5, #ACB6E5);
        color: #000000;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background-color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Encryption/Decryption Helpers
def xor_encrypt(message, key):
    key_ord = ord(key)
    return ''.join([chr(ord(c) ^ key_ord) for c in message])

def xor_decrypt(message, key):
    key_ord = ord(key)
    return ''.join([chr(ord(c) ^ key_ord) for c in message])

def aes_encrypt(message, key):
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    ct = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct)

def aes_decrypt(encrypted, key):
    encrypted = base64.b64decode(encrypted)
    iv = encrypted[:16]
    ct = encrypted[16:]
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

def to_bits(data):
    return ''.join([format(b, '08b') for b in data])

def from_bits(bits):
    return bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])

# Steganography Functions
def embed_steganography(img, message, xor_key, aes_key):
    xor_encrypted = xor_encrypt(message, xor_key)
    aes_encrypted = aes_encrypt(xor_encrypted, aes_key)
    compressed = zlib.compress(aes_encrypted)
    bits = to_bits(compressed)

    data = np.array(img)
    flat = data.flatten()

    if len(bits) > len(flat):
        raise ValueError("Message too large for image.")

    random.seed(aes_key)
    pos = list(range(len(flat)))
    random.shuffle(pos)

    for i, bit in enumerate(bits):
        flat[pos[i]] = (flat[pos[i]] & ~1) | int(bit)

    new_img = flat.reshape(data.shape)
    return Image.fromarray(new_img.astype(np.uint8))

def extract_steganography(img, xor_key, aes_key):
    data = np.array(img).flatten()
    random.seed(aes_key)
    pos = list(range(len(data)))
    random.shuffle(pos)

    bits = ''.join([str(data[p] & 1) for p in pos])

    for i in range(8, len(bits), 8):
        try:
            byte_chunk = from_bits(bits[:i])
            decompressed = zlib.decompress(byte_chunk)
            aes_decrypted = aes_decrypt(decompressed, aes_key)
            message = xor_decrypt(aes_decrypted, xor_key)
            return message
        except:
            continue
    return None

# Streamlit UI
st.title("🔐 Steganography App with XOR + AES + zlib + LSB")
st.write("Securely hide and retrieve messages in PNG images with layered encryption.")

action = st.sidebar.radio("Choose Action", ["Embed Message", "Extract Message"])

if action == "Embed Message":
    st.header("📝 Embed Secret Message")
    file = st.file_uploader("Upload PNG Image", type="png")
    text = st.text_area("Enter the secret message:")
    xor_key = st.text_input("XOR Key (1 character)", max_chars=1)
    aes_key = st.text_input("AES Key (16 characters)", max_chars=16)

    if st.button("Embed Message"):
        if file and text and xor_key and aes_key and len(aes_key) == 16:
            img = Image.open(file).convert('RGB')
            try:
                stego_img = embed_steganography(img, text, xor_key, aes_key)
                buf = io.BytesIO()
                stego_img.save(buf, format='PNG')
                st.success("✅ Message successfully embedded!")
                st.download_button("Download Stego Image", buf.getvalue(), file_name="stego_image.png")
                st.image(stego_img, caption="Stego Image", use_container_width=True)
            except Exception as e:
                st.error(f"❌ {e}")
        else:
            st.warning("Please provide all inputs and ensure AES key is 16 characters.")

if action == "Extract Message":
    st.header("🔍 Extract Secret Message")
    file = st.file_uploader("Upload Stego PNG Image", type="png")
    xor_key = st.text_input("XOR Key (1 character)", max_chars=1, key="extract_xor")
    aes_key = st.text_input("AES Key (16 characters)", max_chars=16, key="extract_aes")

    if st.button("Extract Message"):
        if file and xor_key and aes_key and len(aes_key) == 16:
            img = Image.open(file).convert('RGB')
            message = extract_steganography(img, xor_key, aes_key)
            if message:
                st.success("✅ Message successfully extracted!")
                st.code(message)
            else:
                st.error("❌ Could not extract the message. Check keys or image.")
        else:
            st.warning("Please provide all inputs and ensure AES key is 16 characters.")
