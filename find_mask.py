from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

SCHARR = np.array([
    [-3 - 3j, 0 - 10j, +3 - 3j],
    [-10 + 0j, 0 + 0j, +10 + 0j],
    [-3 + 3j, 0 + 10j, +3 + 3j]
])
BLURR = np.array([
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]) / 25


def convolve(img, conv_filter):
    sub_shape = (img.shape[0] - conv_filter.shape[0] + 1,
                 img.shape[1] - conv_filter.shape[1] + 1)
    view_shape = tuple(np.subtract(img.shape, sub_shape) + 1) + sub_shape

    strides = img.strides + img.strides
    sub_matrices = np.lib.stride_tricks.as_strided(img, view_shape, strides)

    return np.einsum('ij,ijkl->kl', conv_filter, sub_matrices)


def draw(image, grad, bin_mask, bin_mask_blurred, mask, color):
    fig, (
        (ax_orig, ax_man), (ax_bin, ax_bin_blurred_bin)
    ) = plt.subplots(2, 2, figsize=(20, 10))
    # params = {'cmap':'gray', 'vmin': 0, 'vmax': 255}
    params = {'cmap': 'gray'}

    ax_orig.imshow(image, **params)
    ax_orig.set_title(f'Original {color}')

    ax_man.imshow(np.absolute(grad), **params)
    ax_man.set_title(f'Gradient {color}')

    ax_bin.imshow(bin_mask, **params)
    ax_bin.set_title(f'Binary mask {color}')

    #     ax_bin_blurred.imshow(bin_mask_blurred, **params)
    #     ax_bin_blurred.set_title('Binary mask blurred')

    ax_bin_blurred_bin.imshow(mask, **params)
    ax_bin_blurred_bin.set_title(f'Mask {color}')

    plt.show()


def calc_masks(image, color):
    grad = convolve(image, SCHARR)

    bin_mask = np.array(list(
        map(lambda x: list(map(lambda y: 0 < y <= 50, x)), np.absolute(grad))))
    bin_mask_blurred = convolve(bin_mask, BLURR)

    mask = np.array(list(
        map(lambda x: list(map(lambda y: 0 < y <= 50, x)), bin_mask_blurred)))

    # draw(image, grad, bin_mask, bin_mask_blurred, mask, color)

    return mask


def find_mask(file_name, plot=True):
    with Image.open(file_name) as img:
        image = np.array(img)

    image_red = image[:, :, 0]
    image_green = image[:, :, 1]
    image_blue = image[:, :, 2]

    red_mask = calc_masks(image_red, 'RED')
    green_mask = calc_masks(image_green, 'GREEN')
    blue_mask = calc_masks(image_blue, 'BLUE')

    mask = np.logical_or(np.logical_or(red_mask, green_mask), blue_mask)

    if plot:
        fig, ax = plt.subplots(1, 1, figsize=(20, 10))
        # params = {'cmap':'gray', 'vmin': 0, 'vmax': 255}
        params = {'cmap': 'gray'}
        ax.imshow(mask, **params)
        ax.set_title(f'Mask')
        plt.show()

    im = Image.fromarray(mask)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im.save(f'{file_name}_mask.png')

    return mask


if __name__ == '__main__':
    find_mask('research/images/grad22.png')
