import os, json
import csv
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings
from pathlib import Path
from dateutil.parser import parse
from datetime import datetime, date
from timedate import get_qtr
from django.conf import settings
import requests
import glob
from requests.auth import HTTPBasicAuth
import pickle as pkl

from PIL import Image
from bs4 import BeautifulSoup
from django.core.files.storage import FileSystemStorage

IMAGES_PATH = os.path.join('app', 'data', 'rpt')


def merge_dicts(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value
    return destination

def change_directory_owner(path, uid='ubuntu', gid='root'):
    try:
        uidpwd = pwd.getpwnam(uid).pw_uid
        gidgrp = grp.getgrnam(gid).gr_gid
        r = os.chown(path, uidpwd, gidgrp)
    except:
        pass

def path_exists(fn, fp):
    val = False
    if os.path.exists(os.path.join(settings.BASE_DIR, fp, fn)):
        val = True
    return val

def supermakedirs(path, uid='ubuntu', gid='root', mode=0o777):
    # force refresh
    print('start')
    if os.path.exists(path):
        return path
    else:
        # if not path or os.path.exists(path):
        #    return ''
        os.makedirs(path)
        (head, tail) = os.path.split(path)
        print(head)
        if uid:
            head_par = os.path.abspath(os.path.join(head, os.pardir))
            head_par_par = os.path.abspath(os.path.join(head_par, os.pardir))
            print(head_par)
            print(head_par_par)
            os.chmod(path, mode)
            os.chmod(head_par, mode)
            os.chmod(head_par_par, mode)
            change_directory_owner(head, uid, gid)
            change_directory_owner(head_par, uid, gid)
            change_directory_owner(head_par_par, uid, gid)
        print(path)
        # res = supermakedirs(head, uid, gid, mode)
        # print(res
        # os.mkdir(path)
        # os.chmod(path, mode)
        # res += path
        # print(path
        return path


def get_filepath(subdir, file, replace_pairs=[]):
    thispath = os.path.join(subdir) + '\\'
    thisfile = os.path.join(subdir, file)
    dst_path_error = thispath
    if replace_pairs:
        thispath = thispath.replace('\\', '/')
        for pair in replace_pairs:
            pair_find = pair.split(':')[0]
            pair_replace = pair.split(':')[1]
            thispath = thispath.replace(pair_find, pair_replace)
        thispath = thispath.replace('\\', '/')
        dst_path_error = thispath
    dst_file_error = dst_path_error + str(file)
    return_dict = {'fullpath': dst_file_error, 'subdir': dst_path_error}
    print(return_dict)
    return return_dict


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
    plt.close()


def save_np_data(data, fn='temp.npy', fp='app/data/rpt'):
    np.save(os.path.join(settings.BASE_DIR, fp, fn), data)
    print('saved')


def load_np_data(fn='temp.npy', fp='app/data/rpt'):
    data = np.load(os.path.join(settings.BASE_DIR, fp, fn))
    return data[()]


def save_json(data, fn='temp.json', fp='app/data/words', indent=None):
    with open(os.path.join(settings.BASE_DIR, fp, fn), 'w') as outfile:
        j = json.dump(data, outfile, indent=indent)
    return j

def load_json(fn='temp.json', fp='app/data/words'):
    with open(os.path.join(settings.BASE_DIR, fp, fn), 'r') as outfile:
        j = json.load(outfile)
    return j

def save_pkl(data, fn='temp.pkl', fp='app/data/ncua'):
    with open(os.path.join(settings.BASE_DIR, fp, fn), 'wb') as outfile:
        j = pkl.dump(data, outfile)
    return j

def load_pkl(fn='temp.pkl', fp='app/data/ncua'):
    with open(os.path.join(settings.BASE_DIR, fp, fn), 'rb') as outfile:
        j = pkl.load(outfile)
    return j

def get_list_indices(headers, required_headers):
    '''
    #returns the indices for the Acct_083, Acct_### fields

    '''
    headers = [h.lower() for h in headers]
    list_of_indices = list()
    for headername in required_headers:
        index_number = headers.index(headername)
        list_of_indices.append(index_number)

    return list_of_indices


def save_csv(rows=[], header=[], fn='temp.csv', fp='app/data/rpt', mode='w'):
    with open(os.path.join(settings.BASE_DIR, fp, fn), mode, newline='') as outfile:
        wcsv = csv.writer(outfile, delimiter=',')
        if header:
            wcsv.writerow(header)
        for r in rows:
            wcsv.writerow(r)


def load_csv_data(fn='temp.csv', fp='app/data/ncua', return_header=True, delimiter=None, encoding='utf-8'):
    rows = []
    with open(os.path.join(settings.BASE_DIR, fp, fn), 'r', encoding=encoding) as csvfile:
        csv_reader = csv.reader(csvfile)
        if delimiter:
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
        for row in csv_reader:
            rows.append(row)
    if not return_header:
        rows = rows[1:]
    return rows


def load_file(fn='ups_4662984_1586897502_1586983902.xml', fp='app/data/gb/adhoc', readorwrite='r'):
    with open(os.path.join(settings.BASE_DIR, fp, fn), readorwrite) as f:
        data = f.read()
    f.close()
    return data


def np_savetxt(fn, data, fmt='%1.2f', fp='app/data/test', delimiter=","):
    np.savetxt(os.path.join(settings.BASE_DIR, fp, fn), data, fmt=fmt, delimiter=delimiter)

def opentxt(fn='cu_words.txt', fp='app/data/keywords', mode='r', fullfile=False):
    rows = []
    with open(os.path.join(settings.BASE_DIR, fp, fn)) as f:
        if fullfile:
            rows = f.read()
        else:
            for line in f:
                rows.append(line.strip())
    return rows

def savetxt(rows, fn, fp='app/data/keywords', mode='w'):
    with open(os.path.join(fp, fn), mode) as filehandle:
        for listitem in rows:
            filehandle.write('%s\n' % listitem)

def transform(f, transform_list, d):
    # print(f)
    for t in transform_list:
        if t == 'strip':
            d[f] = d[f].strip()
        if 'exists' in t:
            replace_value = t.split('::')
            d[f] = replace_value
            if replace_value[1] == 'None':
                d[f] = None
        if 'replace' in t:
            command, replace_this, with_this = t.split('::')
            if d[f]:
                d[f] = d[f].replace(replace_this, with_this)
        if t == 'datetime':
            d[f] = parse(d[f])
        if t == 'date':
            #print(d, f)
            d[f] = parse(d[f]).date()
        if t == 'year':
            d[f] = d[f].year
        if t == 'month':
            d[f] = d[f].month
        if t == 'day':
            d[f] = d[f].day
        if t == 'title':
            d[f] = d[f].title()
        if t == 'lower':
            #print(f)
            #print(d)
            #print(d[f])
            d[f] = d[f].lower()
        if t == 'upper':
            d[f] = d[f].upper()
    return d


def get_unique_mapping(mapping_dict):
    mapping = {}
    for key, value in mapping_dict.items():
        if key != value:
            mapping[key] = value
    return mapping


def map_fields(rows, headers, mapping_dict, transforms=None,
               improve_performance_using_unique_mappings_fields_only=True):
    mapped_dicts = []
    #if len(headers) == 1:
    #    headers = "".join(headers).split("\t")
    headers = [h.lower() for h in headers]
    if improve_performance_using_unique_mappings_fields_only:
        mapping_dict = get_unique_mapping(mapping_dict)
    for r in rows:
        #if len(r) == 1:
        #    r = "".join(r).split("\t")
        d = dict(zip(headers, r))
        for h in headers:
            if h in mapping_dict:
                #print(h)
                if improve_performance_using_unique_mappings_fields_only:
                    d[mapping_dict[h]] = d[h]
                    del d[h]
            else:
                d.pop(h, None)
        if transforms:
            for f, transform_list in transforms.items():
                #print(f)
                d = transform(f, transform_list, d)
        mapped_dicts.append(d)
    return mapped_dicts


def map_fields_for_data_summary(date_str, table, mapping, rows, entity_type, period):
    """This is for mapping to the data summary

    """
    ml_lists = []
    csv_field_names = [*mapping]
    indices = get_list_indices(rows[0], csv_field_names)
    without_cunumber = indices[1:]
    for row in rows[1:]:
        number = row[indices[0]]
        list_of_summaries = []

        for i, field in enumerate(csv_field_names[1:]):
            d = {}
            d['base_data_interval'] = period

            d['entity_id'] = int(number) if number != '' else 0
            d['entity_type'] = entity_type
            d['series'] = mapping[field]
            d['series_id'] = field
            quarter_value = date_str.split('-')[-1]
            _q = get_qtr(quarter_value)
            d[_q] = float(row[without_cunumber[i]]) if not isinstance(row[without_cunumber[i]], str) else 0.0
            # we need to convert it to year
            d['year'] = int(date_str[:4])
            list_of_summaries.append(d)
        # return DataSummary().import_data(list_of_summaries)
        ml_lists.append(list_of_summaries)
    return ml_lists

def traverse_dir(fn, fp, extensions=['.jpg', '.jpeg', '.png', '.webp'], normalize=False):
    data = []
    final_path = fp
    if fn:
        final_path = os.path.join(fp, fn)
    for root, dirs, files in os.walk(final_path):
        for file in files:
            if file.endswith(tuple(extensions)):
                newfile = os.path.join(root, file)
                if normalize:
                    newfile = normalize_scrape_path(newfile)
                data.append(newfile)
    return data

def get_encoding(file):
    rawdata = open(file, 'rb').read()
    result = chardet.detect(rawdata)
    return result['encoding']

def get_images_in_page(file, return_soup=False, strip_params=True):
    with open(file, encoding='utf8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    imgs = soup.find_all('img')
    if return_soup:
        return imgs
    if not strip_params:
        return [img.get('src') for img in imgs if img.get('src')]
    return [img.get('src').split('?')[0] for img in imgs if img.get('src')]

def get_image_count(files, count_threshold=0, strip_list=['../'], get_extra_data=True):
    from google_tools import remove_domain_name, predict_url_category
    id = {}
    for file in files:
        print(file)
        imgs = get_images_in_page(file, return_soup=get_extra_data)
        for img in imgs:
            if get_extra_data:
                soup = img
                img = soup.get('src')
            if img:
                img = img.split('?')[0]
                for strip in strip_list:
                    if strip in img:
                        img = img.replace(strip, '')
                if not img.startswith('http') and not img.startswith('/'):
                    img = '/' + img
                if img in id:
                    id[img]['count'] += 1
                else:
                    id[img] = {'width':None, 'height':None, 'count':1, 'page':normalize_scrape_path(file)}
                catfile = predict_url_category(file)
                cat = predict_url_category(img)
                if catfile:
                    id[img]['page_category'] = catfile['guessed_category']
                    id[img]['page_subcategory'] = catfile['guessed_subcategory']
                    id[img]['is_biz'] = catfile['is_biz']
                if cat:
                    id[img]['category'] = cat['guessed_category']
                    id[img]['subcategory'] = cat['guessed_subcategory']
                    #id[img]['is_biz'] = cat['is_biz']
                if get_extra_data:
                    alt_text = soup.get('alt')
                    if alt_text:
                        id[img]['alt_text'] = alt_text[:254]
    if count_threshold != 0:
        id_small = dict(id)
        for k,v in id.items():
            if v['count'] > count_threshold:
                id_small.pop(k, None)
        id = id_small
    return id

def get_image_item(file):
    image = Image.open(file)
    width, height = image.size
    return width, height

def get_image_dict(files, key='width', strip_list=['../'], normalize=True):
    id = {}
    for file in files:
        width, height = get_image_item(file)
        #print(width, file)
        newfile = file
        if normalize:
            newfile = normalize_scrape_path(file, strip_list)
        if key == 'width':
            if width not in id:
                id[width] = {}
            if height not in id[width]:
                id[width][height] = []
            id[width][height].append(newfile)
        elif key == 'path':
            if file not in id:
                id[newfile] = {'width':width, 'height':height}
    return id

def normalize_scrape_path(pg, strip_list=['../']):
    if '\\' in pg:
        segs = pg.split('\\')
    else:
        segs = pg.split('/')
    p = '/' + ('/').join(segs[1:])
    for strip in strip_list:
        if strip in p:
            p = p.replace(strip, '')
    if p and p[0] != '/':
        p = '/' + p
    elif not p:
        p = '/'
    return p

def normalize_scrape_paths(files, strip_list=['../']):
    nfiles = []
    for file in files:
        nfiles.append(normalize_scrape_path(file, strip_list))
    return nfiles

def get_dir(fn, fp):
    final_path = fp
    for root, dirs, files in os.walk(final_path):
        for dir in dirs:
            if dir == fn:
                return(os.path.join(root, dir))

def upload_file(co, file_obj, path):
    fs = FileSystemStorage()
    supermakedirs(path)
    file_name, file_ext = os.path.splitext(file_obj.name)
    file_full_name = '%s/%s%s'%(path, file_name, file_ext)
    saved_file = fs.save(file_full_name, file_obj)
    return '%s'%fs.url(saved_file)


def save_img_from_url(fn, fp, url_path, headers={'User-Agent': 'Mozilla/5.0'}, username=None, password=None):
    kwargs = {
        'url':url_path,
        'headers':headers,
        'stream':True,
        }
    if username and password:
        kwargs['auth'] = HTTPBasicAuth(username, password)
    r = requests.get(**kwargs)
    if r.status_code == 200:
        d = supermakedirs(fp)
        if fn:
            fp = os.path.join(fp, fn).replace('\\', '/')
        with open(fp, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        print('saved', fp)
    return os.path.join(fp)

def glob_files(fp, recursive=True, sort_by='-date'):
    dir_array = []
    reverseit = False
    #key = None
    #if sort_by.startswith('-'):
    #    reverseit = True
    #if 'date' in sort_by:
    #    key = os.path.getmtime
    #elif 'size' in sort_by:
    #    key = os.path.getsize

    dirs = glob.glob(fp, recursive=recursive)

    if recursive:
        for dir in dirs:
            new_path = os.path.join(dir, '*')
            dir_count = glob_files(fp=new_path, recursive=False)
            len_dir_count = 0
            if dir_count:
                len_dir_count = len(dir_count)
            dir_array.append(
                {'dir_location':dir, 'count':len_dir_count}
            )
        return dir_array
    #if key:
    #    dirs = sorted(dirs, key=lambda file: key(file))
    #if reverseit:
    #    dirs = dirs.reverse()
    return dirs