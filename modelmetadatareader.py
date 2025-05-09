import os
import json
import torch
import safetensors
import datetime

class ModelMetadataReader:
    CATEGORY = "Model Tools"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("STRING", {"default": "Enter full model path here", "trigger": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_metadata"

    def get_metadata(self, model_path):
        """Retrieves metadata from a model file with enhanced logging."""

        log_entries = []
        log_entries.append(f"📌 Starting Metadata Extraction: {self.get_timestamp()}")
        log_entries.append(f"🔎 Checking model path: {model_path}")

        if not os.path.exists(model_path):
            log_entries.append("❌ Error: Model not found.")
            return ("\n".join(log_entries),)

        metadata = {}

        # ✅ Extract metadata based on file type
        if model_path.endswith(".safetensors"):
            metadata = self.read_safetensors_metadata(model_path)
            log_entries.append("📂 Metadata extraction method: Safetensors")
        elif model_path.endswith((".ckpt", ".pth", ".pt", ".bin")):
            metadata = self.read_torch_metadata(model_path)
            log_entries.append("📂 Metadata extraction method: Checkpoint/Torch")
        else:
            metadata = {"error": "Unsupported model format"}
            log_entries.append("⚠ Unsupported model format detected.")

        log_entries.append(f"✅ Extraction Complete: {self.get_timestamp()}")

        return ("\n".join(log_entries) + "\n\n" + json.dumps(metadata, indent=4),)

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

    def get_timestamp(self):
        """Returns formatted timestamp."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

NODE_CLASS_MAPPINGS = {
    "ModelMetadataReader": ModelMetadataReader
}
