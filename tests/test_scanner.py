import os
import pickle
import pytest
from src.scanner import scan_pickle_file

class DummyExploit:
    def __reduce__(self):
        return (os.system, ("echo 'test exploit'",))

def test_safe_model(tmp_path):
    """Test that a benign pickle file passes the scanner (returns False for suspicious)."""
    safe_file = tmp_path / "safe.pkl"
    safe_data = {"weights": [1.0, 2.0, 3.0]}
    
    with open(safe_file, "wb") as f:
        pickle.dump(safe_data, f)
        
    # Should be clean (not suspicious)
    assert scan_pickle_file(str(safe_file)) == False

def test_exploit_model(tmp_path):
    """Test that a malicious pickle file triggers the scanner (returns True for suspicious)."""
    exploit_file = tmp_path / "exploit.pkl"
    exploit_data = {"weights": DummyExploit()}
    
    with open(exploit_file, "wb") as f:
        pickle.dump(exploit_data, f)
        
    # Should flag as suspicious
    assert scan_pickle_file(str(exploit_file)) == True