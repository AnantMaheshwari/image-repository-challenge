import math
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.cluster import KMeans
from scipy.spatial import distance
import ntpath


class ImagesRepoModel:
    """A class to store different views of the image repository"""

    """ arbitrarily chosen global image size, to allow for easy image comparison """
    IMG_WIDTH = 320
    IMG_HEIGHT = 240

    def __validate_image(self, image_path):
        valid_formats = ('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif')
        if not image_path.lower().endswith(valid_formats):
            raise ValueError
        img = Image.open(image_path)
        img.verify()

    def __compute_image_hashes(self, flattened_image_pixels):
        """ Bitwise XOR based hash of the RGB image pixels """

        img_hash = 0
        i = 0
        while i < self.IMG_WIDTH * self.IMG_HEIGHT * 3:
            """ compute sum of a chunk of pixels"""
            chunk_sum = 0
            for j in range(self.IMG_WIDTH):
                chunk_sum = chunk_sum + flattened_image_pixels[i + j]
            """ bitwise XOR between chunk sums"""
            img_hash = img_hash ^ chunk_sum
            i = i + self.IMG_WIDTH
        return img_hash

    def __define_image_space(self, pic):
        """ Account for comparing greyscale, coloured, and multi-sized images
            by normalizing all pictures to be RGB formatted with the same size. """

        img = Image.open(pic).convert('RGB')
        img = img.resize((self.IMG_WIDTH, self.IMG_HEIGHT))

        """ flatten pixel values """
        img_converted = np.array(img)
        pixel_row = img_converted.ravel()
        pixel_row_as_list = np.array(pixel_row.tolist())

        """ compute hash of image pixels """
        img_hash = self.__compute_image_hashes(pixel_row_as_list)

        return pixel_row_as_list, img_hash

    def __init__(self, image_folder=None, parent=None):
        """ Initialize the image repository using images in image_folder.
            Store names of image to allow for textual searching, and cluster the
            current images to allow for image-based searching """

        self.image_names = []
        self.parent = parent

        for image in image_folder:
            try:
                self.__validate_image(image)
                self.image_names.append(image)
            except (IOError, SyntaxError, ValueError):
                print('Bad image file, not including in repository: ', image)

        self.images_hash = []

        """ Construct matrix where there is a row per image, and columns representing pixel values.
            Note that there is 3*IMG_WIDTH*IMG_HEIGHT columns, since each pixel contributes 3 values (RGB) """
        self.df = pd.DataFrame(index=self.image_names, columns=np.arange(3 * self.IMG_WIDTH * self.IMG_HEIGHT))

        for pic in self.image_names:
            pixel_features, img_hash = self.__define_image_space(pic)
            self.df.loc[pic] = pixel_features
            self.images_hash.append([pic, img_hash])

        """ Cluster images such that they can be searched against """
        self.kmeans = KMeans(n_clusters=math.ceil(math.sqrt(len(self.image_names)))).fit(self.df)


    def text_search(self, query_string):
        """ Finds all images in the repository that have query_string as a substring of their filenmae"""

        print("Searching image repository based on inputted text query: " + query_string)

        search_results = list(filter(lambda k: query_string in ntpath.basename(k), self.image_names))
        if not search_results:
            print("No search results found")
            return self
        print("Found some hits! Now constructing new image repository view with your results...")

        filtered_repo = ImagesRepoModel(search_results, self)
        print(str(len(search_results)) + " Search Result(s): ")
        print(*filtered_repo.image_names, sep="\n")

        print("You are now in a view of the repository containing only the above search results.")
        return filtered_repo

    def image_search(self, query_image):
        """ Search for similar pictures to the image at path query_image,
        by finding images in the precomputed (KMeans) cluster corresponding to the
        centroid with the minimum euclidean distance to the query_image pixel vector"""

        print("Searching image repository for similar images based on query image: " + query_image)

        try:
            self.__validate_image(query_image)
        except (IOError, SyntaxError, ValueError):
            print('Inputted image is not valid: ', query_image)
            return self
        centroids = self.kmeans.cluster_centers_
        labels = self.kmeans.labels_

        pixel_features, img_hash = self.__define_image_space(query_image)

        min_distance = float('inf')
        cluster_belongs = -1
        for index, centroid in enumerate(centroids):
            dist_to_centroid = distance.euclidean(centroid, pixel_features)
            if dist_to_centroid < min_distance:
                min_distance = dist_to_centroid
                cluster_belongs = index

        search_results = []
        for index, name in enumerate(self.image_names):
            if labels[index] == cluster_belongs:
                search_results.append(name)

        if not search_results:
            print("No search results found")
            return self
        print("Found some hits! Now constructing new image repository view with your results...")

        filtered_repo = ImagesRepoModel(search_results, self)
        print(str(len(search_results)) + " Search Result(s): ")
        print(*filtered_repo.image_names, sep="\n")

        print("You are now in a view of the repository containing only the above search results.")
        return filtered_repo

    def check_for_corruption(self):
        """ Compare current and original images hashes to determine
         if any images in the repository have been modified """

        for img_path_and_hash in self.images_hash:
            orig_img_path = img_path_and_hash[0]
            orig_img_hash = img_path_and_hash[1]
            current_pixel_features, current_img_hash = self.__define_image_space(orig_img_path)
            if orig_img_hash != current_img_hash:
                print("Corrupted image! " + orig_img_path)
