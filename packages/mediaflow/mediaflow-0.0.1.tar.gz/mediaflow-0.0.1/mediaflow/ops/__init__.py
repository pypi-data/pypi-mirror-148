import os
from posixpath import abspath
import requests
import json
import magic
import tarfile
import time

processor_list_url = 'http://pai-eas-internet.cn-shanghai.aliyuncs.com/api/v2/public/processors'
processor_url = 'http://pai-eas-internet.cn-shanghai.aliyuncs.com/api/services/resources?type=processor&name='
eas_online = False

model_directory = os.path.join(os.getcwd(), 'model')
if os.getenv('WORKER_NAME') == 'easworker':
    model_directory = '/home/admin/docker_ml/workspace/model'
    eas_online = True


def image_audio_separater(args):
    """
    brief: Split video and audio streams into two channels
    """
    outputs = ['image', 'audio']
    if 'outputs' in args:
        outputs = ','.join(args['outputs'])
    config = {
        'type': 'ImageAudioSeparater',
        'outputs': ','.join(outputs['outputs']),
        'name': 'image_audio_separater',
        'language': 'cpp'
    }
    if args:
        config.update(args)
    return config


def untar_file(src, dest):
    tar = tarfile.open(src)
    tar.extractall(path=dest)
    tar.close()


def downloadfile(url, path):
    if not os.path.exists(path):
        os.mkdir(path)

    start = time.time()
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception("Erorr: Download file (%s) failed, error code: %d"
                        % (url, response.status_code))
    size = 0
    chunk_size = 4096
    content_size = int(response.headers['content-length'])
    print('[INFO] Start download: %s, File size:%.2f MB' %
          (url, content_size / chunk_size / 1024))
    file_name = url.split("/")[-1]
    filepath = os.path.join(path, file_name)
    with open(filepath, 'wb') as file:
        for data in response.iter_content(chunk_size=chunk_size):
            file.write(data)
            size += len(data)
            if os.getenv('WORKER_NAME') != 'easworker':
                print('\r'+'Downloading:%s%.2f%%' % ('>'*int(size*50 /
                                                             content_size), float(size / content_size * 100)), end=' ')
    end = time.time()
    print('completed!,times: %.2f seconds' % (end - start))
    return filepath


def find_entry_path(root, entry):
    list_dirs = os.walk(root)
    for root, dirs, files in list_dirs:
        for f in files:
            if f == entry:
                return os.path.join(root, f)
    raise Exception('Could not find entry: %s at %s' % (entry, root))


def transfer_processor_entry(processor_path, kws):
    if not os.path.exists(processor_path):
        return
    if 'processor_entry' in kws and len(kws['processor_entry']) > 0:
        if not kws['processor_entry'].startswith('/'):
            processor_entry_path = find_entry_path(processor_path,
                                                   kws['processor_entry'])
            kws['processor_entry'] = processor_entry_path
            print('[INFO] find processor entry: %s' % (processor_entry_path))


def custom_process(kws, processors_path):
    if eas_online:
        transfer_processor_entry(processors_path, kws)
        return

    download_processor_url = kws['processor_path']
    if not download_processor_url.startswith('http'):
        raise Exception('Custom processor only support http url.')
    processor = os.path.splitext(download_processor_url.split('/')[-1])[0]
    processor_flag = os.path.join(processors_path, processor+'_exist')
    processor_path = os.path.join(processors_path, processor)

    if os.path.exists(processor_flag):
        transfer_processor_entry(processor_path, kws)
        print('[INFO] Processor %s already exist, not update.' % (processor))
        return

    download_file = downloadfile(
        download_processor_url, processor_path)

    # uncompress processor
    mime = magic.from_file(download_file, mime=True)
    if mime in "application/x-gzip application/gzip application/x-tar".split():
        untar_file(download_file, processor_path)
        os.remove(download_file)

    transfer_processor_entry(processor_path, kws)
    # touch a flag file
    fd = open(processor_flag, 'w')
    fd.close()


def builtin_process(kws, processors_path):
    processor = kws['processor']
    if processor == 'tensorflow':
        processor = 'tensorflow_cpu_1.15'
    elif processor == 'pytorch':
        processor = 'pytorch_cpu_1.6'

    processor_config = os.path.join(
        processors_path, kws['name']+".config")

    # download processor
    if not eas_online:
        r = requests.get(processor_list_url)
        if r.status_code != 200:
            raise Exception("request process list list failed: %s" %
                            (processor_list_url))
        content_json = json.loads(r.text)
        support_processor_list = []
        for item in content_json['Processors']:
            support_processor_list.append(item['ProcessorName'])
        if processor not in support_processor_list:
            raise Exception("Not support processor: %s" % (processor))

        processor_config_url = processor_url + processor
        r = requests.get(processor_config_url)
        if r.status_code != 200:
            raise Exception("request process config failed: %s" %
                            (processor_config_url))
        text = r.text
        with open(processor_config, 'w') as fd:
            fd.write(text)
        processor_config_json = json.loads(text)
    else:
        if not os.path.exists(processor_config):
            raise Exception('processor config: %s does not exist.' %
                            (processor_config))
        with open(processor_config, 'r') as fd:
            text = fd.read()
            processor_config_json = json.loads(text)

    kws.update(processor_config_json)
    custom_process(kws, processors_path)


def model_process(kws):
    download_model_url = kws['model_path']
    if download_model_url.startswith('http'):
        download_file = downloadfile(download_model_url, model_directory)
        # uncompress processor
        mime = magic.from_file(download_file, mime=True)
        if mime in "application/x-gzip application/gzip application/x-tar".split():
            untar_file(download_file, model_directory)
            os.remove(download_file)
        kws['model_path'] = model_directory
        return


def create_processor(lang, name, **kws):
    config = {}
    if lang == 'cpp':
        config['op_type'] = 'CppProcessor'
    elif lang == 'java':
        config['op_type'] = 'JavaProcessor'
    elif lang == 'go':
        config['op_type'] = 'GoProcessor'
    else:
        raise Exception('Only support cpp, java and go processor.')

    config['name'] = name
    kws['name'] = name
    config['async_interface'] = 'True'

    # all op and processor should be put the directory processors.
    processors_path = os.path.join(os.getcwd(), 'processors')
    if not eas_online and not os.path.exists(processors_path):
        os.mkdir(processors_path)

    # custom processor
    if 'processor_path' in kws:
        custom_process(kws, processors_path)
    # built-in processor
    elif 'processor' in kws:
        builtin_process(kws, processors_path)

    if 'model_path' in kws:
        model_process(kws)

    for key, value in kws.items():
        config[key] = str(value)

    return config
