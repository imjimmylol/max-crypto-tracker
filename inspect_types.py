import inspect
import sys


def main() -> None:
    """Inspect the Telethon library to find Forum/Topic related types."""
    print(f"--- Inspecting Telethon Types in {sys.executable} ---")

    try:
        import telethon.tl.types as all_types

        print("\nSuccessfully imported telethon.tl.types. Searching for types...")
        print("=" * 70)

        count = 0
        for name, obj in inspect.getmembers(all_types):
            if inspect.isclass(obj) and ("Forum" in name or "Topic" in name):
                print(f"Found matching type: {name}")
                count += 1

        if count == 0:
            print("\nNo types containing 'Forum' or 'Topic' were found.")
        else:
            print(f"\nFound {count} matching types.")

        print("=" * 70)

    except ImportError:
        print("\nError: Could not import the 'telethon' library.")
        print(
            "Please ensure it is installed in the 'crypto-signal-tracker' "
            "conda environment."
        )

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
