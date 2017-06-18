import zipfile

import os
from django.http import HttpResponse
from concrete_project.settings import BASE_DIR
import shutil


# Create your views here.
# https://stackoverflow.com/questions/14438928/python-zip-a-sub-folder-and-not-the-entire-folder-path
def makeArchive(fileList, archive, root):
    """
    'fileList' is a list of file names - full path each name
    'archive' is the file name for the archive with a full path
    """
    a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)

    for f in fileList:
        print("archiving file %s" % f)
        a.write(f, os.path.relpath(f, root))
    a.write(os.path.relpath(os.path.join(BASE_DIR, 'db.sqlite3')))
    a.close()


def dirEntries(dir_name, subdir, *args):
    # Creates a list of all files in the folder
    '''Return a list of file names found in directory 'dir_name'
    If 'subdir' is True, recursively access subdirectories under 'dir_name'.
    Additional arguments, if any, are file extensions to match filenames. Matched
        file names are added to the list.
    If there are no additional arguments, all files found in the directory are
        added to the list.
    Example usage: fileList = dirEntries(r'H:\TEMP', False, 'txt', 'py')
        Only files with 'txt' and 'py' extensions will be added to the list.
    Example usage: fileList = dirEntries(r'H:\TEMP', True)
        All files and all the files in subdirectories under H:\TEMP will be added
        to the list. '''

    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            if not args:
                fileList.append(dirfile)
            else:
                if os.path.splitext(dirfile)[1][1:] in args:
                    fileList.append(dirfile)
            # recursively access file names in subdirectories
        elif os.path.isdir(dirfile) and subdir:
            print("Accessing directory:", dirfile)
            fileList.extend(dirEntries(dirfile, subdir, *args))
    return fileList


def email_website_folder(request):
    folder = os.path.join(BASE_DIR, 'media')
    save_to_location = os.path.join(BASE_DIR, 'utility/temp')
    zipname = 'jeff_test.zip'
    os.chdir(os.path.join(BASE_DIR, 'utility/temp'))
    makeArchive(dirEntries(folder, True), zipname, save_to_location)
    return HttpResponse('this is the email site to admin view')

