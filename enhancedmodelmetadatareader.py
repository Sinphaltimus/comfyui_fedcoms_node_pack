import os
import re
import json
import datetime

class EnhancedModelMetadataReader:
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
        """Extracts metadata and raw text from an ONNX file with enhanced logging."""
        
        log_entries = []
        log_entries.append(f"📌 Starting Metadata Extraction: {self.get_timestamp()}")
        log_entries.append(f"🔎 Checking model path: {model_path}")

        if not os.path.exists(model_path):
            log_entries.append("❌ Error: Model not found.")
            return ("\n".join(log_entries),)

        # ✅ Extract Metadata and Raw Text from ONNX
        metadata, raw_text = self.extract_onnx_metadata(model_path)
        log_entries.append("📂 Metadata extraction method: Direct Binary Parsing")
        
        log_entries.append(f"✅ Extraction Complete: {self.get_timestamp()}")

        return ("\n".join(log_entries) + "\n\n" + json.dumps(metadata, indent=4) + "\n\n🔍 Extracted Raw Text:\n" + raw_text[:2000],)

    def extract_onnx_metadata(self, file_path):
        """Extracts readable metadata and raw text from an ONNX file using direct binary parsing."""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            # Extract human-readable text sections
            extracted_text = re.findall(rb'[ -~]{4,}', data)  # Captures ASCII-readable characters
            decoded_text = [text.decode("utf-8", errors="ignore") for text in extracted_text]

            # Look for potential metadata-related fields
            metadata_keys = ["author", "description", "license", "version", "model_name"]
            metadata_found = {key: value for value in decoded_text if any(key in value.lower() for key in metadata_keys)}

            # Combine raw extracted text
            raw_text_output = "\n".join(decoded_text)

            return metadata_found if metadata_found else {"warning": "No structured metadata found."}, raw_text_output

        except Exception as e:
            return {"error": f"Failed to extract metadata: {str(e)}"}, ""

    def get_timestamp(self):
        """Returns formatted timestamp."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

NODE_CLASS_MAPPINGS = {
    "EnhancedModelMetadataReader": EnhancedModelMetadataReader
}
