def inspect_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        
    print(f"--- Inspection Report for {file_path} ---")
    print(f"Total Size: {len(data)} bytes")
    
    # Check for common hidden file signatures
    signatures = {
        b'PK\x03\x04': "ZIP archive",
        b'\x89PNG': "Hidden PNG",
        b'Rar!': "RAR archive",
        b'\x7fELF': "Linux Executable",
        b'BZh': "BZIP2 compression"
    }
    
    for sig, name in signatures.items():
        if sig in data:
            print(f"[!] ALERT: {name} signature found at offset {data.find(sig)}")

    # Check for trailing data after the JPEG End of Image (FF D9) marker
    eoi_marker = b'\xff\xd9'
    eoi_index = data.rfind(eoi_marker)
    if eoi_index != -1 and eoi_index < len(data) - 2:
        print(f"[!] ALERT: Appended data found after JPEG EOI marker ({len(data) - eoi_index - 2} bytes)")

inspect_file('reality_debugger.jpeg')

# Found ZIP signature at offset 59082, indicating hidden ZIP data appended to the JPEG. Let's extract it.

input_file = 'reality_debugger.jpeg'
output_file = 'hidden_payload.zip'
offset = 59082

with open(input_file, 'rb') as f:
    f.seek(offset)
    zip_data = f.read()

with open(output_file, 'wb') as f:
    f.write(zip_data)

print(f"Success! Extracted {len(zip_data)} bytes to {output_file}")
