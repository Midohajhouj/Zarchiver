import os
import tarfile
import zipfile
import gzip
import bz2
import lzma
import argparse
from pathlib import Path
import shutil
import hashlib
import logging
import sys
from colorlog import ColoredFormatter  # For colored logging

class CompressionError(Exception):
    """Custom error class for compression-related errors."""
    pass

def setup_logging(verbose: bool) -> None:
    """Setup logging with colors based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO

    # Create a colored formatter
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    # Create a stream handler and set the formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Configure the root logger
    logging.root.setLevel(level)
    logging.root.addHandler(handler)

def validate_input_path(input_path: str) -> None:
    """Validate that the input path exists."""
    if not Path(input_path).exists():
        raise CompressionError(f"Input path does not exist: {input_path}")

def validate_output_path(output_path: str) -> None:
    """Validate that the output path is valid and does not overwrite existing files."""
    if Path(output_path).exists():
        raise CompressionError(f"Output path already exists: {output_path}")

def calculate_checksum(file_path: str, algorithm: str = 'sha256') -> str:
    """Calculate the checksum of a file."""
    hash_algo = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def compress_file(input_path: str, output_path: str, format: str, level: int, verbose: bool) -> None:
    """Compress a single file."""
    validate_input_path(input_path)
    validate_output_path(output_path)

    logging.info(f"Compressing file: {input_path} to {output_path} with format {format}")

    with open(input_path, 'rb') as f_in:
        data = f_in.read()

    if format == 'gz':
        with gzip.open(output_path, 'wb', compresslevel=level) as f_out:
            f_out.write(data)
    elif format == 'xz':
        with lzma.open(output_path, 'wb', preset=level) as f_out:
            f_out.write(data)
    elif format == 'bz2':
        with bz2.open(output_path, 'wb', compresslevel=level) as f_out:
            f_out.write(data)
    elif format == 'zip':
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=level) as zipf:
            zipf.write(input_path, arcname=os.path.basename(input_path))
    elif format == 'tar':
        with tarfile.open(output_path, 'w') as tar:
            tar.add(input_path, arcname=os.path.basename(input_path))
    elif format == 'zst':  # New format (basic example, not actual Zstandard compression)
        with open(output_path, 'wb') as f_out:
            f_out.write(data)  # Just copy the data as a placeholder
    else:
        raise CompressionError(f"Unsupported format: {format}")

    logging.info("Compression complete")

def compress_directory(input_path: str, output_path: str, format: str, verbose: bool) -> None:
    """Compress a directory."""
    validate_input_path(input_path)
    validate_output_path(output_path)

    logging.info(f"Compressing directory: {input_path} to {output_path} with format {format}")

    if format == 'tar':
        with tarfile.open(output_path, 'w') as tar:
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=input_path)
                    tar.add(file_path, arcname=arcname)
    elif format == 'zip':
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=input_path)
                    zipf.write(file_path, arcname=arcname)
    elif format == 'zst':  # New format (basic example, not actual Zstandard compression)
        with open(output_path, 'wb') as f_out:
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f_in:
                        f_out.write(f_in.read())
    else:
        raise CompressionError(f"Unsupported format for directories: {format}")

    logging.info("Compression complete")

def decompress(input_path: str, output_path: str, verbose: bool) -> None:
    """Decompress a file."""
    validate_input_path(input_path)
    validate_output_path(output_path)

    logging.info(f"Decompressing file: {input_path} to {output_path}")

    if input_path.endswith('.gz'):
        with gzip.open(input_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif input_path.endswith('.xz'):
        with lzma.open(input_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif input_path.endswith('.bz2'):
        with bz2.open(input_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif input_path.endswith('.zip'):
        with zipfile.ZipFile(input_path, 'r') as zipf:
            zipf.extractall(output_path)
    elif input_path.endswith('.tar'):
        with tarfile.open(input_path, 'r') as tar:
            tar.extractall(output_path)
    elif input_path.endswith('.zst'):  # New format (basic example, not actual Zstandard decompression)
        with open(input_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        raise CompressionError(f"Unsupported format: {input_path}")

    logging.info("Decompression complete")

def main() -> None:
    parser = argparse.ArgumentParser(description="A multi-format compression and decompression tool")
    parser.add_argument("-c", "--compress", action="store_true", help="Compress files or directories")
    parser.add_argument("-d", "--decompress", action="store_true", help="Decompress files")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("output", help="Output file or directory")
    parser.add_argument("-f", "--format", choices=["gz", "xz", "bz2", "zip", "tar", "zst"], default="gz", help="Compression format (default: gz)")
    parser.add_argument("-l", "--level", type=int, choices=range(1, 10), default=6, help="Compression level (1-9, default: 6)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    setup_logging(args.verbose)

    try:
        if args.compress:
            input_path = Path(args.input)
            output_path = Path(args.output)

            if input_path.is_dir():
                compress_directory(input_path, output_path, args.format, args.verbose)
            else:
                compress_file(input_path, output_path, args.format, args.level, args.verbose)
        elif args.decompress:
            decompress(args.input, args.output, args.verbose)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        logging.error("\nOperation cancelled by user (Ctrl+C). Exiting gracefully.")
        sys.exit(1)
    except CompressionError as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
