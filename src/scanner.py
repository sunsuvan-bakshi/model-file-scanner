import argparse
import pickletools

# Define dangerous global imports or execution hooks commonly tied to exploits
DANGEROUS_MODULES = {"os", "subprocess", "builtins", "sys"}
DANGEROUS_FUNCTIONS = {"system", "popen", "eval", "exec", "spawn", "execl"} 

def scan_pickle_file(file_path: str) -> bool:
    """
    Statically analyzes a pickle file's byte stream for dangerous opcodes
    without executing any code. Returns True if suspicious, False if clean.
    """
    print(f"[*] Scanning file: {file_path}")
    
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
            
        # Iterate through the pickle bytecode opcodes safely
        # pickletools.genops yields a tuple of (opcode, argument, position)
        suspicious_found = False
        
        for opcode, arg, pos in pickletools.genops(file_content):
            # GLOBAL and STACK_GLOBAL opcodes reference external modules and functions (e.g., os.system)
            if opcode.name in ("GLOBAL", "STACK_GLOBAL", "INST", "OBJ"):
                print(f"  [!] Found global reference: {arg} at position {pos}")

                # Convert arg to string representation to catch nested modules/functions
                arg_str = str(arg).lower()
                
                # Check if a dangerous module + function combination appears
                for mod in DANGEROUS_MODULES:
                    for func in DANGEROUS_FUNCTIONS:
                        if mod in arg_str and func in arg_str:
                            print(f"  [ALERT] Hazardous execution vector matched: '{mod}.{func}' found in arg '{arg}'")
                            suspicious_found = True

            # Also check if REDUCE opcode is present (used to execute function with arguments)
            if opcode.name == "REDUCE":
                print(f"  [!] Found REDUCE execution opcode at position {pos}")
                print(f"  [ALERT] Hazardous execution trigger ('REDUCE') detected!")
                suspicious_found = True

        return suspicious_found

    except Exception as e:
        print(f"[ERROR] Failed to parse file {file_path}: {e}")
        return True # Fail secure on corruption/read errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "MLSecOps Model File Scanner")
    parser.add_argument("--target", required = True, help = "Path to the model file to scan")
    args = parser.parse_args()
    
    is_suspicious = scan_pickle_file(args.target)
    
    if is_suspicious:
        print("\n[RESULT] ❌ SECURITY WARNING: Suspicious execution vectors found!")
        exit(1)
    else:
        print("\n[RESULT] ✅ CLEAN: No hazardous opcodes detected.")
        exit(0)