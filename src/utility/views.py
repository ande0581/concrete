from concrete_project.settings import BASE_DIR, NEXTCLOUD_URL, NEXTCLOUD_USER, NEXTCLOUD_PASSWORD
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

import owncloud
import os
import shutil
import tempfile
import zipfile
from datetime import date


def upload_to_next_cloud(file=None):
    filename = 'madsen_concrete/madsen_concrete_archive_{}.zip'.format(date.today().strftime("%Y_%m_%d"))
    oc = owncloud.Client(NEXTCLOUD_URL)
    oc.login(NEXTCLOUD_USER, NEXTCLOUD_PASSWORD)
    oc.put_file(filename, file)


def upload_website(request):
    media_folder = os.path.join(BASE_DIR, 'media')
    sql_db = os.path.join(BASE_DIR, 'db.sqlite3')
    with tempfile.TemporaryDirectory() as td:
        tmparchive = os.path.join(td, 'archive')
        shutil.make_archive(base_name=tmparchive, format='zip', root_dir=media_folder, base_dir="./")

        zf = zipfile.ZipFile(os.path.join(td, 'archive.zip'), mode='a')
        zf.write(sql_db, arcname=os.path.basename(sql_db))
        zf.close()

        try:
            upload_to_next_cloud(file=os.path.join(td, 'archive.zip'))
            messages.success(request, "Website Data Uploaded")
        except:
            messages.error(request, "Upload Failed")

    return HttpResponseRedirect('/utility')


class UtilityList(LoginRequiredMixin, TemplateView, SuccessMessageMixin):
    template_name = 'utility/utility_list.html'

