from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from find_mask import find_mask


def white_dot(value):
    return value == 255


def find_borders(i, j, image):
    n, m = image.shape
    i_border = i
    j_border = j
    for k in range(i + 1, n):
        if not white_dot(image[k, j]):
            break
        i_border = k
    for l in range(j + 1, m):
        if not white_dot(image[i, l]):
            break
        j_border = l
    return i_border, j_border


def check_rectangle(i1, j1, i2, j2, image):
    is_filled_rectangle = np.all(white_dot(image[i1:i2 + 1, j1:j2 + 1]))
    if is_filled_rectangle:
        image[i1:i2 + 1, j1:j2 + 1] = 100
    return is_filled_rectangle


def find_rectangles(image_orig):
    image = np.copy(image_orig)
    n, m = image.shape
    THRESHOLD = min(n, m) // 50
    rectangles = []

    try:
        for i in range(n):
            # if i % 10 == 0:
            #     print(f'i={i}')
            for j in range(m):
                #             if j % 10 == 0:
                #                 print(f'j={j}')

                #                 if not any(white_dot(image[:, j])):
                #                     continue

                if white_dot(image[i, j]):
                    i_border, j_border = find_borders(i, j, image)
                    # if i > 1000:
                    #     print(f'check', i, j, i_border, j_border)
                    if i_border - i >= THRESHOLD and j_border - j >= THRESHOLD:

                        found = check_rectangle(i, j, i_border, j_border,
                                                image)
                        if found:
                            rectangles.append((i, j, i_border, j_border))
                            # print(
                            #     f'Found rectangle #{len(rectangles)}: {i, j}, {i_border, j_border}')
                            if len(rectangles) >= 11:
                                return rectangles, image
        #                 else:
        #                     if i > 1000:
        #                         print(f'point not white: {image[i, j]}', i, j)
        return rectangles, image
    except KeyboardInterrupt:
        return rectangles, image


def plot_results(rectangles, image_orig, image_mask, modified_img):
    fig, ax_orig = plt.subplots(1, 1, figsize=(20, 10))
    params = {'cmap': 'gray', 'vmin': 0, 'vmax': 255}

    ax_orig.imshow(image_orig)
    ax_orig.set_title('Original')

    for rect in rectangles:
        ax_orig.add_patch(
            patches.Rectangle((rect[1] + 0, rect[0] + 0), rect[3] - rect[1],
                              rect[2] - rect[0], linewidth=1, edgecolor='r',
                              facecolor='none'))

    plt.show()


def find_coordinates(mask, image_orig, plot=True):
    mask = np.array(list(map(lambda x: list(map(lambda y: 255 if y else 0, x)), mask)))
    rectangles, img = find_rectangles(mask)

    if plot:
        plot_results(rectangles, image_orig, mask, img)


if __name__ == '__main__':
    names = [
        # 'research/images/grad12.png',
        # 'research/images/grad22.png',
        'research/images/grad30.png',
        # ('images/grad12_res_man.png', 'images/grad12.png'),
        # ('images/grad13.png', 'images/grad13.png'),
        # ('research/images/grad12_mask.png', 'research/images/grad12.png'),
        # ('research/images/grad20_mask.png', 'research/images/grad12.png'),
        # ('research/images/grad12_mask.png', 'research/images/grad12.png'),
        # ('research/images/grad12_mask.png', 'research/images/grad12.png'),
        # ('images/grad15_mask.png', 'images/grad15.png'),
    ]

    for name in names:
        with Image.open(name) as im:
            image_orig = np.array(im)
        mask = find_mask(name)
        find_coordinates(mask, image_orig)
