import sys

from ppm import PythonPackageManager


def main(argv: list):
	ppm = PythonPackageManager()
	ppm.main(argv)


if __name__ == '__main__':
	main(sys.argv[1:])
