# generateData.py
import random

def generateDataFile(filename="input.dat", lines=100):
    """
    Generates a file with numerical data for processing.
    - Positive integers are valid data.
    - Negative integers simulate hardware read errors (data corruption).
    - The number 999 is a trigger for a software bug (segfault in C).
    - The number 0 is a trigger for a recoverable software error.
    """
    with open(filename, 'w') as f:
        # Ensure specific failure cases are present
        failurePoints = [-10, 0, 999, -25]
        for i in range(lines - len(failurePoints)):
            f.write(f"{random.randint(1, 100)}\n")
        
        # Intersperse failure points
        for point in failurePoints:
             f.write(f"{point}\n")
    print(f"Generated '{filename}' with {lines} lines.")

if __name__ == "__main__":
    generateDataFile()