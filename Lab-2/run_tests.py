import glob
import os
import subprocess
import sys

def main() -> None:
    input_files = sorted(glob.glob(os.path.join("test", "*.input.txt")))
    if not input_files:
        print("No test files were found in the test/*.input.txt")
        sys.exit(1)

    passed = 0
    failed = 0

    for input_path in input_files:
        expected_path = input_path.replace(".input.txt", ".expected.txt")
        test_name = os.path.basename(input_path).replace(".inpur.txt", "")

        if not os.path.exists(expected_path):
            print(f"[Missing Expected] {test_name}")
            failed += 1
            continue

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read().rstrip("\r\n")

        result = subprocess.run(
            [sys.executable, "parser.py", input_path],
            capture_output=True,
            text=True,
            encoding="utf-8", 
            )
        actual_output = result.stdout.rstrip("\r\n")

        if actual_output == expected_output:
            print(f"[Pass] {test_name}")
            passed += 1
        else:
            print(f"[Fail] {test_name}")
            print("  Expected:")
            for line in expected_output.splitlines():
                print("  {line}")
                print("  Actual:")
            for line in actual_output.splitlines():
                print(f"{line}")
                failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed out of {passed + failed} tests.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
