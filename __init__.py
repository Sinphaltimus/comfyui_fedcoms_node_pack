from .modelmetadatareader import ModelMetadataReader
from .modeldataextractor import ModelDataExtractor
from .enhancedmodelmetadatareader import EnhancedModelMetadataReader  # ✅ New Node Added

NODE_CLASS_MAPPINGS = {
    "ModelMetadataReader": ModelMetadataReader,
    "ModelDataExtractor": ModelDataExtractor,
    "EnhancedModelMetadataReader": EnhancedModelMetadataReader,  # ✅ Third Node Included
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelMetadataReader": "Model Metadata Reader",
    "ModelDataExtractor": "Advanced Model Data Extractor",
    "EnhancedModelMetadataReader": "Enhanced Model Metadata Reader",  # ✅ Custom UI Label
}
