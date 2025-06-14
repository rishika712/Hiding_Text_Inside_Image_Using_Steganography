import streamlit as st
from PIL import Image
import numpy as np
import zlib
import random

def embed_steganography(image_path, message, key, output_path):
    # Load image
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    flat_data = data.flatten()
    
    # Encrypt + compress
    xor_encrypted = xor_encrypt(message.encode('utf-8'), key)
    compressed = zlib.compress(xor_encrypted)
    
    # Append delimiter
    compressed += b'###END###'
    
    bits = text_to_bits(compressed)
    
    if len(bits) > len(flat_data):
        raise ValueError("Message too large for this image!")
    
    # Generate pseudo-random positions
    random.seed(ord(key))  # key-based seed
    positions = list(range(len(flat_data)))
    random.shuffle(positions)
    
    # Embed bits in random LSB positions
    for i, bit in enumerate(bits):
        pos = positions[i]
        flat_data[pos] = (flat_data[pos] & 254) | int(bit)

    
    # Save new image
    new_data = flat_data.reshape(data.shape)
    stego_img = Image.fromarray(new_data.astype(np.uint8))
    stego_img.save(output_path)
    print(f"✅ Message embedded and saved as: {output_path}")
def extract_steganography(image_path, key):
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    flat_data = data.flatten()
    
    # Generate pseudo-random positions
    random.seed(ord(key))
    positions = list(range(len(flat_data)))
    random.shuffle(positions)
    
    # Extract bits
    bits = ''
    for pos in positions:
        bits += str(flat_data[pos] & 1)
        if len(bits) % 8 == 0:
            # Check for delimiter
            current_bytes = bits_to_bytes(bits)
            if b'###END###' in current_bytes:
                break
    
    # Remove delimiter
    extracted_bytes = bits_to_bytes(bits)
    extracted_bytes = extracted_bytes.replace(b'###END###', b'')
    
    # Decompress + decrypt
    decompressed = zlib.decompress(extracted_bytes)
    decrypted = xor_decrypt(decompressed, key)
    
    return decrypted.decode('utf-8')

def text_to_bits(text):
    return ''.join(format(byte, '08b') for byte in text)

def bits_to_bytes(bits):
    return bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])

def xor_encrypt(text, key):
    return bytes([b ^ ord(key) for b in text])

def xor_decrypt(encrypted_bytes, key):
    return bytes([b ^ ord(key) for b in encrypted_bytes])

def embed_steganography(image, message, key):
    data = np.array(image)
    flat_data = data.flatten()

    xor_encrypted = xor_encrypt(message.encode('utf-8'), key)
    compressed = zlib.compress(xor_encrypted)
    compressed += b'###END###'
    bits = text_to_bits(compressed)

    if len(bits) > len(flat_data):
        st.error("❌ Message too large for this image!")
        return None

    random.seed(ord(key))
    positions = list(range(len(flat_data)))
    random.shuffle(positions)

    for i, bit in enumerate(bits):
        pos = positions[i]
        flat_data[pos] = (flat_data[pos] & 254) | int(bit)

    new_data = flat_data.reshape(data.shape)
    stego_img = Image.fromarray(new_data.astype(np.uint8))
    return stego_img

def extract_steganography(image, key):
    data = np.array(image)
    flat_data = data.flatten()

    random.seed(ord(key))
    positions = list(range(len(flat_data)))
    random.shuffle(positions)

    bits = ''
    for pos in positions:
        bits += str(flat_data[pos] & 1)
        if len(bits) % 8 == 0:
            current_bytes = bits_to_bytes(bits)
            if b'###END###' in current_bytes:
                break

    extracted_bytes = bits_to_bytes(bits).replace(b'###END###', b'')
    decompressed = zlib.decompress(extracted_bytes)
    decrypted = xor_decrypt(decompressed, key)
    return decrypted.decode('utf-8')

# Streamlit UI
st.title("🔐 Image Steganography - Hide & Extract Text")

menu = st.sidebar.selectbox("Choose Mode", ["Hide Text", "Extract Text"])

if menu == "Hide Text":
    uploaded_file = st.file_uploader("Upload a PNG image", type=['png'])
    secret_text = st.text_area("Enter the text to hide")
    key = st.text_input("Enter a single character key", max_chars=1)

    if st.button("Embed Text"):
        if uploaded_file and secret_text and key:
            img = Image.open(uploaded_file).convert('RGB')
            stego_img = embed_steganography(img, secret_text, key)
            if stego_img:
                st.image(stego_img, caption='Stego Image')
                stego_img.save("stego_output.png")
                with open("stego_output.png", "rb") as f:
                    st.download_button("Download Stego Image", f, file_name="stego_output.png")
        else:
            st.warning("Please provide image, text, and key!")

if menu == "Extract Text":
    uploaded_file = st.file_uploader("Upload the stego PNG image", type=['png'])
    key = st.text_input("Enter the key used for embedding", max_chars=1)

    if st.button("Extract Text"):
        if uploaded_file and key:
            img = Image.open(uploaded_file).convert('RGB')
            try:
                hidden_text = extract_steganography(img, key)
                st.success("Hidden text successfully extracted!")
                st.code(hidden_text)
            except Exception as e:
                st.error(f"Extraction failed: {e}")
        else:
            st.warning("Please provide image and key!")
