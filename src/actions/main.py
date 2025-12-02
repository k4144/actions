import os

os.environ["VERSION"] = "1.0.0"


def main():
    return os.environ["VERSION"]


if __name__ == "__main__":
    main()
