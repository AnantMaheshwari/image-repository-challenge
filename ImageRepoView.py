import sys
from sys import stdin
import os
from ImageRepoModel import ImagesRepoModel

def generate_image_paths(image_folder):
    return [os.path.join(image_folder, image) for image in os.listdir(image_folder)]

def user_prompt():
    print("Type \"search text\" to search within the current view of the image repository")
    print("Type \"search images\" to search within the current view of the image repository")
    print("Type \"return\" to get back to the previous search result")
    print("Type \"return home\" to get back to the original image repository")
    print("Type \"check for corruption\" to check whether any image in the current view has been corrupted")

def image_repo_interface(model):
    user_prompt()
    searching_text = False
    searching_images = False
    for line in stdin:
        if line == '':
            break
        line = line.strip()
        if searching_text is True:
            model = model.text_search(line)
            searching_text = False
            user_prompt()
        elif searching_images is True:
            model = model.image_search(line)
            searching_images = False
            user_prompt()
        elif line == 'search text':
            searching_text = True
            print("Type the query text string you wish to search with")
        elif line == 'search images':
            searching_images = True
            print("Type the path to the image you wish to search with")
        elif line == 'return':
            if model.parent:
                model = model.parent
                print("Back to previous search results: ")
                print(*model.image_names, sep=", ")
            else:
                print("Already at original image repository, cannot return back further")
            user_prompt()
        elif line == 'return home':
            if not model.parent:
                print("Already at original image repository, cannot return back further")
            while model.parent:
                model = model.parent
            print("At original image repository.\n")
            user_prompt()
        elif line == 'check for corruption':
            model.check_for_corruption()
            user_prompt()
        else:
            print("Command not recognized. Check your spelling :)")
            user_prompt()


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Invalid number of arguments")
        sys.exit()
    image_directory = sys.argv[1]
    if not os.path.exists(image_directory):
        print("Image directory path argument is not a valid path")
        sys.exit()

    image_paths = generate_image_paths(image_directory)
    print("Building image repository and clustering images for searching, wait a few moments...")
    model = ImagesRepoModel(image_paths)
    image_repo_interface(model)


