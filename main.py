from argparse import ArgumentParser
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from find_coordinates import find_coordinates
from find_mask import find_mask


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="File name of the image", metavar="FILE")
    parser.add_argument("-p", "--no-plot", dest="no_plot", default=True,
                        action="store_false",
                        help="Plot results via matplotlib")
    parser.add_argument("-c", "--coordinates", dest="coordinates", default=False,
                        action="store_true",
                        help="Plot results via matplotlib")

    args = parser.parse_args()
    print(args)

    mask = find_mask(args.filename)

    if args.coordinates:
        with Image.open(args.filename) as im:
            image_orig = np.array(im)
        find_coordinates(mask, image_orig)


if __name__ == '__main__':
    main()
