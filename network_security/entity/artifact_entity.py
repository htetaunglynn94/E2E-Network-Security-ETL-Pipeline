from dataclasses import dataclass # decorator for data classes

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
    
