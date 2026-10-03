# PDF Encrypt/Decrypt Tool

Encrypt or decrypt PDF files with password protection and permissions control.

## Features

- **Encrypt PDFs**: Add password protection to PDF files
- **Decrypt PDFs**: Remove encryption with correct password
- **Permission Control**: Fine-grained control over PDF permissions
- **Batch Processing**: Encrypt multiple files at once
- **Check Status**: View encryption status of PDFs
- **Auto-Detect**: Automatically detect encrypt or decrypt mode

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Encrypt a PDF

```bash
python pdf-encrypt.py input.pdf output.pdf --encrypt
```

Interactive password prompt:
```bash
python pdf-encrypt.py input.pdf output.pdf -e
```

With explicit password:
```bash
python pdf-encrypt.py input.pdf output.pdf -e -p MyPassword123
```

### Decrypt a PDF

```bash
python pdf-encrypt.py encrypted.pdf decrypted.pdf --decrypt
```

With password:
```bash
python pdf-encrypt.py encrypted.pdf decrypted.pdf -d -p MyPassword123
```

### Remove Password Protection

```bash
python pdf-encrypt.py protected.pdf unprotected.pdf --remove
```

### Check Encryption Status

```bash
python pdf-encrypt.py document.pdf --check
```

### Batch Encrypt

```bash
python pdf-encrypt.py file1.pdf file2.pdf file3.pdf -o encrypted/ -e -p secret
```

## Options

| Option | Description |
|--------|-------------|
| `-e, --encrypt` | Encrypt the PDF |
| `-d, --decrypt` | Decrypt the PDF |
| `-r, --remove` | Remove password protection |
| `-p, --password` | Password (prompted if not provided) |
| `-o, --output-dir` | Output directory for batch operations |
| `--check` | Check encryption status |
| `--user-password` | Separate user password (optional) |
| `--suffix` | Suffix for batch output (default: _encrypted) |
| `--no-print` | Disable printing in encrypted PDF |
| `--no-copy` | Disable copying in encrypted PDF |
| `--no-modify` | Disable modifications in encrypted PDF |

## Permission Options

When encrypting, you can restrict what users can do:

| Option | Effect |
|--------|--------|
| `--no-print` | Users cannot print |
| `--no-copy` | Users cannot copy text |
| `--no-modify` | Users cannot modify the PDF |

## Security Notes

- **User vs Owner Password**: The user password is required to open the PDF. The owner password (same as user by default) controls permissions.
- **Strong Passwords**: Use strong, unique passwords for better security.
- **Permissions**: Permissions are advisory - determined PDFs may still be circumvented.

## Examples

### Create Read-Only PDF

```bash
python pdf-encrypt.py input.pdf readonly.pdf -e -p pass --no-print --no-copy --no-modify
```

### Encrypt with Separate User Password

```bash
python pdf-encrypt.py input.pdf output.pdf -e -p owner_pass --user-password user_pass
```

### Decrypt Multiple Files

```bash
python pdf-encrypt.py file1.pdf file2.pdf -o decrypted/ -d -p secret
```

## Requirements

- Python 3.8+
- PyPDF2 - PDF manipulation library
