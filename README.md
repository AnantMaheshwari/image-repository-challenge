# Shopify Challenge: Image Repository


## Overview

This program provides a command line interface to interact with an image repository. 
The main focus is supporting searching the image repository using both query strings and query images, and searching at multiple levels (e.g. searching within previous search results).
## Usage
We will a small subset of the iris flower dataset to show off some features. This contains a mix of daisy, dandelion, rose, sunflower and tulip pictures :)

```terminal
python ImageRepoView.py /path/to/folder/with/images
Building image repository and clustering images for searching, wait a few moments...
```

Upon startup, all the images in the passed in folder */path/to/folder/with/images* are clustered (KMeans) using their pixel values such that they can be efficiently searched against.

```terminal
Type "search text" to search within the current view of the image repository
Type "search images" to search within the current view of the image repository
Type "return" to get back to the previous search result
Type "return home" to get back to the original image repository
```

**search text**: Searches using the provided query string against all the image repository file names (checking if the query is a substring of any image file names), and finds any search hits.

**search images**: Using KMeans clustering, uses the provided query image path (user inputs a path to an image), and finds any "similar" images in the repository.

**return**: Return to the previous search result (zoom out of current search level)

**return home**: Return to the original view of the image repository

```terminal
$ search text
Type the query text string you wish to search with
$ tulip
Searching image repository based on inputted text query...
Found some hits! Now constructing new image repository view with your results...
Search results: 
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6770436217_281da51e49_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6539831765_c21b68910e_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6808860548_53796b90ca_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6325571510_7544b27e57_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6799076717_575944af91_m.jpg
You are now in a view of the repository containing only the above search results.
```

As we can see, we found some images with filenames containing tulip. Also, notice that we are now within the search results, so we can perform another search to find a specific tulip.

```terminal
$ search text
Type the query text string you wish to search with
$ c21b68910e_n
Searching image repository based on inputted text query...
Found some hits! Now constructing new image repository view with your results...
Search results: 
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6539831765_c21b68910e_n.jpg
You are now in a view of the repository containing only the above search results.
```

Now, let's zoom back out and return to the original repository. We will do this using "return home", however note that using "return" twice would accomplish the same thing.

```terminal
$ return home
At original image repository.
```

Now, for something cool let's consider if we wanted to search our image repository purely using a query picture, and our repository of pictures (not using any labelling).
This can be thought of like a google image search, except you pass in a photo as your search query instead of text. 
We'll use a sunflower picture from our dataset:
![alt text](/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg?raw=true) and search it against the dataset, we should expect to get some sunflowers as search hits!

```terminal
$ search images
Type the path to the image you wish to search with
$ /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg
Searching image repository for similar images...
Found some hits! Now constructing new image repository view with your results...
Search results:
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16967372357_15b1b9a812_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/dandelion_4151883194_e45505934d_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16988605969_570329ff20_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_17148843706_df148301ac_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_17433282043_441b0a07f4_n.jpg, /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/dandelion_4226758402_a1b75ce3ac_n.jpg 
```

![alt text](/IrisDataVerySmall/sunflower_16967372357_15b1b9a812_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/dandelion_4151883194_e45505934d_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_16988605969_570329ff20_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_17148843706_df148301ac_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_17433282043_441b0a07f4_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/dandelion_4226758402_a1b75ce3ac_n.jpg?raw=true)


We can see we got a all of the sunflowers in the dataset, as well as some dandelions which appear to share some general shape with the sunflowers.
Note that from here we could now perform another search using another image query, or a text query, to further narrow down results.

## Next Directions