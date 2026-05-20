"""
Encrypts and decrypts API keys at rest using Fernet symmetric encryption.
Run `python key_manager.py` once to encrypt your keys from .env into .env.encrypted.
The app reads from .env.encrypted at runtime — never stores plaintext keys in code.
"""
import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet

KEY_FILE = Path(__file__).parent.parent / ".secret.key"
ENC_FILE = Path(__file__).parent.parent / ".env.encrypted"


def generate_key() -> bytes:
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    print(f"Encryption key saved to {KEY_FILE}")
    return key


def load_key() -> bytes:
    if not KEY_FILE.exists():
        raise FileNotFoundError(
            f"Encryption key not found at {KEY_FILE}. Run: python key_manager.py"
        )
    return KEY_FILE.read_bytes()


def encrypt_env(env_path: Path) -> None:
    key = generate_key() if not KEY_FILE.exists() else load_key()
    f = Fernet(key)

    lines = env_path.read_text().splitlines()
    encrypted_lines = []
    for line in lines:
        if "=" in line and not line.startswith("#"):
            var, val = line.split("=", 1)
            encrypted_val = f.encrypt(val.strip().encode()).decode()
            encrypted_lines.append(f"{var}={encrypted_val}")
        else:
            encrypted_lines.append(line)

    ENC_FILE.write_text("\n".join(encrypted_lines))
    print(f"Encrypted env saved to {ENC_FILE}")


def load_encrypted_env() -> dict[str, str]:
    if not ENC_FILE.exists():
        return {}

    key = load_key()
    f = Fernet(key)
    env: dict[str, str] = {}

    for line in ENC_FILE.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            var, val = line.split("=", 1)
            try:
                env[var.strip()] = f.decrypt(val.strip().encode()).decode()
            except Exception:
                env[var.strip()] = val.strip()
    return env


def get_secret(key_name: str) -> str:
    encrypted_env = load_encrypted_env()
    if key_name in encrypted_env:
        return encrypted_env[key_name]
    val = os.environ.get(key_name, "")
    if not val:
        raise ValueError(f"Secret '{key_name}' not found in encrypted env or environment variables.")
    return val


if __name__ == "__main__":
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        print(f"No .env file found at {env_file}. Create it first.")
        sys.exit(1)
    encrypt_env(env_file)
    print("Done! Your API keys are now encrypted.")
    print(f"Keep {KEY_FILE} secret — add it to .gitignore.")
