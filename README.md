# ZArchiver

ZArchiver is a versatile, multi-format compression and decompression tool designed for efficiency and ease of use. It supports a wide range of file formats, making it the perfect choice for managing archives in various formats, including `.gz`, `.xz`, `.bz2`, `.zip`, `.tar`, `.7z`, and `.rar`.

---

## 🚀 Features

- **Compression Formats:** Supports gzip (`.gz`), bzip2 (`.bz2`), xz (`.xz`), zip (`.zip`), tar (`.tar`), and 7z (`.7z`).
- **Decompression Formats:** Handles gzip, bzip2, xz, zip, tar, 7z, and rar archives.
- **Checksum Validation:** Generate file checksums using SHA256.
- **Compression Levels:** Adjustable compression levels for formats like gzip, xz, and bzip2.
- **Logging:** Verbose mode for detailed logging during operations.

---

## 🔧 Installation

### Requirements

- Python 3.7+
- Required Libraries:
  - `tqdm`
  - `py7zr`
  - `rarfile`

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Midohajhouj/ZArchiver.git
   cd ZArchiver
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📜 Usage

Run ZArchiver from the command line for compressing and decompressing files or directories.

### Compress Files or Directories

```bash
python zarchiver.py compress <input_path> <output_path> -f <format> -l <level> -v
```

- `<input_path>`: Path to the file or directory to compress.
- `<output_path>`: Destination file for the compressed archive.
- `-f <format>`: Compression format (`gz`, `xz`, `bz2`, `zip`, `tar`, `7z`). Default is `gz`.
- `-l <level>`: Compression level (1-9). Default is `6`.
- `-v`: Enable verbose output.

#### Example:

Compress a file into gzip format:
```bash
python zarchiver.py compress file.txt file.txt.gz -f gz -l 9 -v
```

### Decompress Files

```bash
python zarchiver.py decompress <input_path> <output_path> -v
```

- `<input_path>`: Path to the compressed archive.
- `<output_path>`: Destination file or directory for decompression.
- `-v`: Enable verbose output.

#### Example:

Decompress a gzip file:
```bash
python zarchiver.py decompress file.txt.gz file.txt -v
```

---

## 🎯 Supported Formats

| Format | Compression | Decompression |
|--------|-------------|---------------|
| `.gz`  | ✅          | ✅            |
| `.xz`  | ✅          | ✅            |
| `.bz2` | ✅          | ✅            |
| `.zip` | ✅          | ✅            |
| `.tar` | ✅          | ✅            |
| `.7z`  | ✅          | ✅            |
| `.rar` | ❌          | ✅            |

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

#### *<p align="center">Coded by <a href="https://github.com/Midohajhouj">LIONMAD</a></p>*
