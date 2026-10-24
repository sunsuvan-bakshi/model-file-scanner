# Model File Scanner 🛡️

A lightweight MLSecOps security utility designed to inspect serialized machine learning model files (such as PyTorch `.pt` and Python `pickle` files) for unsafe deserialization bytecode opcodes **before** they can execute arbitrary system code.

---

## 🚨 Threat Model & Motivation

In machine learning pipelines, pulling pre-trained model weights from open registries carries a hidden supply chain risk. Standard deserialization methods (like Python's `pickle.load()`) implicitly execute embedded byte instructions upon loading. 

An attacker can weaponize a model weight file by embedding a malicious payload using opcodes like `GLOBAL` or `REDUCE` to trigger system commands (e.g., reverse shells or file extraction) the moment the model is loaded into memory. 

This project solves this by introducing a **static analysis security gate** that disassembles model files safely using `pickletools` without executing code, flagging hazardous instructions beforehand.

---

## 🛠️ Tech Stack & Architecture

* **Language:** Python 3.10+
* **Core Modules:** `pickletools`, `io`, `argparse`
* **DevSecOps & Pipeline:** Docker, GitHub Actions (CI/CD integration)
* **Testing:** Pytest

---

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone (https://github.com/sunsuvan-bakshi/model-file-scanner.git)
   cd model-file-scanner

2. **Set up a virtual environment:**
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

3. **Install dependencies:**
pip install -r requirements.txt

---

## 🚀 Usage

Run the scanner against a target model file to inspect its bytecode opcodes:

python src/scanner.py --target path/to/model.pt

Exit Code 0: File is safe (no hazardous import/execution opcodes found).
Exit Code 1: Security warning triggered (suspicious execution hooks detected).

---

## 🧪 Running Tests

To verify detection accuracy against safe and simulated exploit payloads:

pytest tests/

---

## 🗺️ Roadmap & Future Enhancements

[ ] Add support for parsing SafeTensors and ONNX structural manifests.
[ ] Implement a containerized Docker workflow for local scanning.
[ ] Complete GitHub Actions CI/CD pipeline integration to block pull requests containing malicious artifacts.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you would like to change or submit a Pull Request.

---

## 📄 License

Distributed under the MIT License. See LICENSE for more information.