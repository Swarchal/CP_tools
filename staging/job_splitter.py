from parserix import parse
import pandas as pd

def job_splitter(img_list, job_size=96):
    """split imagelist into an imagelist per job containing job_size images"""
    df_img = _well_site_table(img_list)
    grouped_list = _group_images(df_img)
    return [chunk for chunk in chunks(grouped_list, job_size)]


def remove_crap(img_list, ext=".tif"):
    """remove non-images and thumbnails from image list"""
    return [i for i in img_list if i.endswith(ext) and "thumb" not in i]


def _group_images(df_img):
    """group images by well and site"""
    grouped_list = []
    for _, group in  df_img.groupby(["Metadata_well", "Metadata_site"]):
        grouped = list(group["img_paths"])
        channel_nums = [parse.img_channel(i) for i in grouped]
        # create tuple (path, channel_number) and sort by channel number
        sort_im = sorted(list(zip(grouped, channel_nums)), key=lambda x: x[1])
        # return on the file-paths back from the list of tuples
        grouped_list.append([i[0] for i in sort_im])
    return grouped_list


def _well_site_table(imglist):
    """return pandas dataframe with metadata columns"""
    final_files = [parse.img_filename(i) for i in imglist]
    df_img = pd.DataFrame({
        "img_paths"     : imglist,
        "Metadata_well" : [parse.img_well(i) for i in final_files],
        "Metadata_site" : [parse.img_site(i) for i in final_files]
        })
    return df_img


def chunks(list_like, job_size):
    for i in range(0, len(list_like), job_size):
        yield list_like[i:i+job_size]
