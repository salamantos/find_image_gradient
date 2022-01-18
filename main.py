from argparse import ArgumentParser
from PIL import Image
import numpy as np

from find_coordinates import find_coordinates
from find_mask import find_mask


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="File name of the image", metavar="FILE")
    parser.add_argument("-p", "--plot", dest="plot", default=False,
                        action="store_true",
                        help="Plot results via matplotlib")
    parser.add_argument("-c", "--coordinates", dest="coordinates", default=False,
                        action="store_true",
                        help="Plot results via matplotlib")

    args = parser.parse_args()

    mask = find_mask(
        args.filename,
        plot=(args.plot and not args.coordinates),
    )

    if args.coordinates:
        with Image.open(args.filename) as img:
            image_orig = np.array(img)
        find_coordinates(mask, image_orig, plot=args.plot)


if __name__ == '__main__':
    main()
