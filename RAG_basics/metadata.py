
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal
from uuid import NAMESPACE_URL, uuid5

Visibility  = Literal["public","internal"]


@dataclass (frozen = False)
class MetadataEnrichment:
    visibility: Visibility = "internal"  
    title : str = None
    source_type: str = None

    def enrich_metadata(self,metadata: dict):
        timestamp = datetime.now(timezone.utc).isoformat()
        source = metadata.get("source", self.title or "unknown-source")
        source_key = str(source).replace("\\", "/").casefold()
        stable_document_id = uuid5(NAMESPACE_URL, source_key)

        metadata.update({
            "visibility": self.visibility,
            "created_at": timestamp,
            "updated_at": timestamp,
            "document_id" : str(stable_document_id),
            "title" : self.title
        })
        if self.source_type is not None:
            metadata["source_type"] = self.source_type

        return metadata
