import os
import json
import torch
import safetensors
import chardet
import datetime

class ModelDataExtractor:
    CATEGORY = "Model Tools"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("STRING", {"default": "Enter full model path here", "trigger": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "extract_data"

    def extract_data(self, model_path):
        """Extracts metadata and raw text with enhanced logging."""

        log_entries = []
        log_entries.append(f"📌 Starting Data Extraction: {self.get_timestamp()}")
        log_entries.append(f"🔎 Checking model path: {model_path}")

        if not os.path.exists(model_path):
            log_entries.append("❌ Error: Model not found.")
            return ("\n".join(log_entries),)

        extracted_data = {}

        # ✅ Extract structured metadata based on model format
        if model_path.endswith(".safetensors"):
            extracted_data["structured_metadata"] = self.read_safetensors_metadata(model_path)
            log_entries.append("📂 Metadata extraction method: Safetensors")
        elif model_path.endswith((".ckpt", ".pth", ".pt", ".bin", ".gguf", ".onnx")):
            extracted_data["structured_metadata"] = self.read_torch_metadata(model_path)
            log_entries.append("📂 Metadata extraction method: Checkpoint/Torch")

        # ✅ Always attempt raw text extraction
        extracted_data["raw_text"] = self.extract_raw_text(model_path)
        log_entries.append("📂 Attempting raw text extraction.")

        log_entries.append(f"✅ Extraction Complete: {self.get_timestamp()}")

        return ("\n".join(log_entries) + "\n\n" + json.dumps(extracted_data, indent=4),)

    def read_safetensors_metadata(self, model_path):
        """Reads metadata from Safetensors models."""
        try:
            with safetensors.safe_open(model_path, framework="pt") as f:
                return f.metadata()
        except Exception as e:
            return {"error": f"Safetensors extraction failed: {str(e)}"}

    def read_torch_metadata(self, model_path):
        """Reads metadata from Torch-based models."""
        try:
            model_data = torch.load(model_path, map_location="cpu")
            return {"metadata_keys": list(model_data.keys())}
        except Exception as e:
            return {"error": f"Torch model extraction failed: {str(e)}"}

    def extract_raw_text(self, model_path):
        """Attempts raw text extraction from model binaries."""
        try:
            with open(model_path, "rb") as f:
                data = f.read()
                encoding = chardet.detect(data)["encoding"]
                text_data = data.decode(encoding, errors="ignore") if encoding else "Encoding not detected"
            
            return text_data[:2000]  # ✅ Increased limit for better visibility
        except Exception as e:
            return f"Error extracting raw text: {str(e)}"

    def get_timestamp(self):
        """Returns formatted timestamp."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

NODE_CLASS_MAPPINGS = {
    "ModelDataExtractor": ModelDataExtractor
}
