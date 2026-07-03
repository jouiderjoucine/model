import hashlib
import os

salt = bytes.fromhex("ca3363ea29bf3979b73b8178d3528e40")

CHECKPOINT_FILE = "checkpointrsndom.txt"
OUTPUT_FILE = "fileranfom.txt"

# Resume if possible
if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "r") as f:
        password_str = f.read().strip()
    print("Resuming from:", password_str)
else:
    password_str = "faeff75b5198a44e"
    print("Starting from:", password_str)

while True:
    password = password_str.encode()

    key = hashlib.pbkdf2_hmac(
        "sha256",
        password,
        salt,
        32800,
        dklen=32,
    )

    check = bytearray(key[:8])

    # XOR the four 8-byte blocks together
    for i in range(8, 32, 8):
        for j in range(8):
            check[j] ^= key[i + j]

    next_password = check.hex()

#    print(f"{password_str} -> {next_password}")

    # Append current pair to file.txt
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"{password_str}\n")
        f.flush()
        os.fsync(f.fileno())

    # Save checkpoint
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(next_password)
        f.flush()
        os.fsync(f.fileno())

    password_str = next_password
