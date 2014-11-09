
import os
import cgi
import sys
import uuid
import json
import ijson
import shutil
import zipfile
import requests
from lbbulk import config
from multiprocessing import Process
from pyramid.view import view_config
from pyramid.response import Response

@view_config(context=Exception)
def error_view(exc, request):
    """ Customized Exception View
    """
    #l = traceback.extract_tb(request.exc_info[2])
    exc_type, exc_obj, exc_tb = sys.exc_info()
    exc_msg = exc_obj.args
    if len(exc_obj.args) > 0:
        exc_msg = exc_obj.args[0]
    return Response(exc_msg, status=500)

def zip_upload(request):

    file_ = request.params.get('file')

    if not isinstance(file_, cgi.FieldStorage):
        return Response('File is not a zip file', status=500)
    else:
        ext_dir, json_file_path = extract_zip(file_)
        process = Process(target=bulk_upload, args=(ext_dir, json_file_path,
            config.LIGHTBASE_URL))
        process.start()

    return Response('OK')

def extract_zip(zfile):

    identifier = str(uuid.uuid4())
    zpath = config.EXTRACT_DIR + '/' + identifier + '.zip'
    zpath = os.path.abspath(zpath)

    try:
        # write bytes to disk
        with open(zpath, 'wb') as f:
            f.write(zfile.file.read())
    except Exception as e:
        raise Exception('Error while uploading file! %s' % e)

    ext_dir =  os.path.abspath(config.EXTRACT_DIR + '/' + identifier)

    if not os.path.exists(ext_dir):
            os.makedirs(ext_dir)

    try:
        # extract zip file 
        with zipfile.ZipFile(zpath, "r") as z:
            z.extractall(ext_dir)
    except Exception as e:
        raise Exception('Error while extracting zip file! %s' % e)

    # remove zip file
    os.remove(zpath)

    json_file_path = ext_dir + '/' + config.JSON_FILENAME
    json_file_path = os.path.abspath(json_file_path)

    if not os.path.exists(json_file_path):
        raise Exception('Could not find any json file in zip file: %s' %
            config.JSON_FILENAME)

    return ext_dir, json_file_path

def bulk_upload(ext_dir, file_path, url):

    file_ = open(file_path, 'rb')

    try:
        objects = ijson.items(file_, 'results.item')
        computers = (computer for computer in objects)
    except Exception as e:
        print('Error While Reading JSON file: %s' % e)

    for computer in computers:
        document = json.dumps(computer)

        response = requests.post(url,
            data={'value': document})

    shutil.rmtree(ext_dir)

