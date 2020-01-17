import cv2, h5py, re, tqdm, os

def list_files(directory, extension='', *, full_path=True, search_subdirectories=False):
    """
    Get all files in a given directory with the given file extension.
    :param directory: directory containing the files
    :param extension: file extension (e.g. '.txt')
    :param full_path: True to return full paths, False to return file names only
    :param search_subdirectories: whether files in subdirectories are returned
    :return: list of files in the given directory
    """
    if search_subdirectories:
        temp = [os.path.join(path, file) for (path, names, file_names) in os.walk(directory) for file in file_names]
        return [i for i in temp if i.endswith(extension)]
    return [f'{directory}/{file}' if full_path else file for file in os.listdir(directory)
            if file.endswith(extension)]

fish_dir = ''
avi_dir = fish_dir + '/processed/avi/'
h5_files = list_files(fish_dir, extension='h5')
fps = 100

for hdf_path in h5_files:
    filename, file_extension = os.path.splitext(hdf_path)
    vid = h5py.File(hdf_path, 'r')
    keys = vid.keys()
    images = []
    dotstop = ''
    for i in keys:
        ind = re.findall('\d+', i)
        images.append(int(ind[0]))
    images = sorted(images)
    video_name = filename + dotstop + '.avi'
    height, width = vid[list(keys)[0]][:].shape

    video = cv2.VideoWriter(os.path.splitext(hdf_path)[0].replace(fish_dir , avi_dir) + '.avi',
                            cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (width, height), isColor=False)
    for im in tqdm(sorted(keys, key=lambda x: int(x))):
        img = vid[im][:]
        video.write(img)

    cv2.destroyAllWindows()
    video.release()