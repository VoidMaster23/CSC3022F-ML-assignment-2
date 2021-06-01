import  sys
from utils import extract_args




if __name__ == "__main__":

    width, height, startPt, endPt, k, gamma = extract_args(sys.argv)
    print(width)
    print(height)
    print(startPt)
    print(endPt)
    print(k)
    print(gamma)