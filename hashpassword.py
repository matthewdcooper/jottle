import sys
import hashlib

def main():
    print("Enter your password: ")
    passbytes = sys.stdin.readline().strip().encode()
    h = hashlib.sha512(passbytes).hexdigest()
    print(h)

if __name__ == "__main__":
    main()
