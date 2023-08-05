import os
import sys
orig_flags = sys.getdlopenflags()  # nopep8
sys.setdlopenflags(os.RTLD_NOW | os.RTLD_GLOBAL)  # nopep8
from . import libmediaflow  # nopep8
sys.setdlopenflags(orig_flags)  # nopep8

from .libmediaflow import MediaGraph
from .libmediaflow import MediaEngine
from .libmediaflow import MediaService
from .libmediaflow import Property

import time
import threading
import pkg_resources
import requests
from graphviz import Digraph
from abc import abstractmethod


default_concurrency = 5


def print_dot_to_ascii(dot: str, fancy: bool = True):
    url = 'https://dot-to-ascii.ggerganov.com/dot-to-ascii.php'
    boxart = 0
    # use nice box drawing char instead of + , | , -
    if fancy:
        boxart = 1
    params = {
        'boxart': boxart,
        'src': dot,
    }
    try:
        response = requests.get(url, params=params).text
        if response == '':
            print('[VISUALIZE_ERROR] DOT string is not formatted correctly')
        print('------ service graph:')
        print(response)
        print('------')
        return True
    except Exception as err:
        return False


class GraphContext:
    def __init__(self):
        self.graph_bak = None
        self.graph = None

    def __enter__(self):
        global _default_graph
        self.graph_bak = _default_graph
        _default_graph = self.graph
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global _default_graph
        _default_graph = self.graph_bak


class Graph():
    def __init__(self, concurrency=default_concurrency):
        self.media_graph = MediaGraph(concurrency)
        self.index = 0
        self.function_index_map = {}
        self.decode_image_index = 0
        self.decode_audio_index = 0
        self.decode_image_audio_index = 0
        self.sort_union_index = 0
        self.merge_index = 0
        self.merge_sequential_index = 0
        self.last_index = 0
        self.encode_index = 0
        self.image_audio_seprate_index = 0
        pass

    def init(self):
        if not self.media_graph.init():
            raise Exception('graph init failed.')

    def get_decode_image_id(self):
        index = self.decode_image_index
        self.decode_image_index += 1
        return str(index)

    def get_decode_audio_id(self):
        index = self.decode_audio_index
        self.decode_audio_index += 1
        return str(index)

    def get_image_audio_seprate_id(self):
        index = self.image_audio_seprate_index
        self.image_audio_seprate_index += 1
        return str(index)

    def get_decode_image_audio_id(self):
        index = self.decode_image_audio_index
        self.decode_image_audio_index += 1
        return str(index)

    def get_sort_union_id(self):
        index = self.sort_union_index
        self.sort_union_index += 1
        return str(index)

    def get_merge_id(self):
        index = self.merge_index
        self.merge_index += 1
        return str(index)

    def get_merge_sequential_id(self):
        index = self.merge_sequential_index
        self.merge_sequential_index += 1
        return str(index)

    def get_last_id(self):
        index = self.last_index
        self.last_index += 1
        return str(index)

    def get_encode_id(self):
        index = self.encode_index
        self.encode_index += 1
        return str(index)

    def get_id(self, function):
        function_keys = self.function_index_map.keys()
        if function in function_keys:
            self.function_index_map[function] += 1
        else:
            self.function_index_map[function] = 0
        return str(self.function_index_map[function])

    def create_input(self, input_name):
        self.media_graph.create_input(input_name)

    def create_op(self, name, op_config={}, args={}):
        assert(isinstance(op_config, dict) == True)
        if len(op_config) != 0:
            for key, value in op_config.items():
                op_config[key] = str(value)
        assert(isinstance(args, dict) == True)
        if len(args) != 0:
            for key, value in args.items():
                args[key] = str(value)
        if not self.media_graph.create_op(name, op_config, args):
            raise Exception('Exception: create op failed.')

    def connect_op(self, source, dest):
        if not self.media_graph.connect_op(source, dest):
            raise Exception('Exception: connect op %s -> %s failed.' %
                            (source, dest))

    def add_op_input(self, op, input):
        if not self.media_graph.add_op_input(op, input):
            raise Exception(
                'Exception: add op(%s) input(%s) failed.' % (op, input))

    def add_op_output(self, op, output):
        if not self.media_graph.add_op_output(op, output):
            raise Exception(
                'Exception: add op(%s) input(%s) output.' % (op, output))

    def add_subgraph(self, name, graph):
        if not self.media_graph.add_subgraph(name, graph.media_graph):
            raise Exception(
                'Exception: add subgraph(%s) failed' % (name))

    def get_op_count(self):
        return self.media_graph.get_op_count()

    def get_input_names(self):
        return self.media_graph.get_input_names()

    def get_all_node_names(self):
        return self.media_graph.get_all_node_names()

    def get_edges(self):
        return self.media_graph.get_edges()

    def get_output_names(self):
        return self.media_graph.get_output_names()

    def visualize(self, graph_name=None, path=None, print_to_ascii=True):
        d_graph = Digraph()
        inputs = self.get_input_names()
        for input in inputs:
            d_graph.node(input, input)
        nodes = self.get_all_node_names()
        for node in nodes:
            d_graph.node(node, node)
        outputs = self.get_output_names()
        for output in outputs:
            d_graph.node(output, output)

        edges = self.get_edges()
        for src, dsts in edges.items():
            for dst in dsts:
                d_graph.edge(src, dst)
        if graph_name and path:
            d_graph.format = 'svg'
            d_graph.render(graph_name, path, view=False)
        if print_to_ascii:
            if not print_dot_to_ascii(d_graph.__str__()):
                print(d_graph)

    def async_visualize(self, graph_name=None, path=None):
        threading.Thread(target=self.visualize, args=(
            graph_name, path,)).start()

    def as_default(self):
        graph_ctx = GraphContext()
        graph_ctx.graph = self
        return graph_ctx

    @staticmethod
    def save(path=None, graph=None):
        if not graph:
            graph = get_default_graph()
        vip_user_id = os.getenv('VIP_USER_ID')
        if vip_user_id is not None:
            vip_path = os.getenv('VIP_PATH')
            if vip_path is None:
                vip_path = '/tmp/vip'
            if not os.path.exists(vip_path):
                os.makedirs(vip_path)
            path = '%s/%s_%d_mediaflow.json' % (vip_path, vip_user_id,
                                                int(time.time()))
        if path is None:
            raise Exception('need set graph file path.')

        if not graph.media_graph.save(path):
            raise Exception('save graph to %s failed.' % path)

    @staticmethod
    def restore(path, concurrency=default_concurrency):
        if not os.path.exists(path):
            raise 'file %s is not is exist.' % path
        new_graph = Graph()
        new_graph.media_graph = MediaGraph.restore(path, concurrency)
        if not new_graph:
            raise 'restore graph from %s failed.' % path
        return new_graph

    @staticmethod
    def restore_as_default(path):
        global _default_graph
        _default_graph = Graph.restore(path)


_default_graph = Graph()


def get_default_graph():
    return _default_graph


class Engine():
    def __init__(self, **options):
        """
        options:
        jvm_options: -Xmx100M -Xms100M
        share_memory_size: 1000(MB)
        enable_numpy: True/Flase
        worker_threads: default 8
        session_policy: 0: wait until a resource is available
                        1: attempts to get resource and returns immediately if there are no resource
                        2: attempts to get the resource, and creates the resource immediately if there is none
        """
        self.engine = MediaEngine(options)

    def run(self, inputs, ctx, graph=None):
        if not graph:
            graph = get_default_graph()

        graph.init()
        return self.engine.run(graph.media_graph, ctx, inputs)


# service plugin
HELPER_CTRLSOCKET = "ctrl_socket"
HELPER_VIPSERVER = "vip_server"
HELPER_LUA = "lua_plugin"
HELPER_COUNTER = "performance_counter"
HELPER_SIGNALHANDLER = "signal_handler"
HELPER_MIRROR = "mirror"
HELPER_HEALTH = "health_check"
HELPER_PLUGIN = "builtin_plugin"


class Service():
    def __init__(self, address, **options):
        """
        options:
        jvm_options: -Xmx100M -Xms100M
        enable_share_memory: True/Flase
        share_memory_size: 8000(MB)
        enable_numpy: True/Flase
        async_service: True/False
        has_one_input: True/False
        output_from_context: True/False
        metric_print: True/False
        worker_threads: default 8
        io_threads: default 4
        token: service token
        need_batch: enable batch service, True/False, default False
        batch_num: batch number, default 16
        batch_timeout: batch timeout, default 100(ms)
        rpc_keepalive: rpc keepalive time, default 5000(ms)
        enable_stream: enalbe stram rpc
        session_policy: 0: wait until a resource is available
                        1: attempts to get resource and returns immediately if there are no resource
                        2: attempts to get the resource, and creates the resource immediately if there is none
        multi_models_metric: True/False, default False
        """
        if os.getenv('WORKER_NAME') == 'easworker':
            address = '0.0.0.0:8080'
        self.media_service = MediaService(address, options)
        self.routers = self.get_router()
        self.graph_map = {"/teardown": ""}
        self.prop = Property()
        self.workspace = self.prop.get('eas.workspace', '')

    def add_graph(self, name, graph):
        self.media_service.add_graph(name, graph.media_graph)
        self.graph_map['/' + name] = graph

    def remove_graph(self, name):
        self.media_service.remove_graph(name)

    def get_router(self):
        return self.media_service.get_router()

    def add_default_graph(self, graph):
        self.media_service.add_default_graph(graph.media_graph)
        self.graph_map['/'] = graph

    def start(self):
        self.media_service.start()

    def stop(self):
        self.media_service.stop()

    def ready_to_wait(self):
        self.media_service.ready_to_wait()

    def warmup(self, binary=b''):
        if binary != b'':
            print('[INFO] warmimg up using local data')
            self.media_service.warmup(
                self.graph_map['/'].media_graph, binary)
            return

        def do_warmup(warm_dir, warm_cnt=5, path='/'):
            print('[INFO] searching warmup files in ', warm_dir)
            for file in os.listdir(warm_dir):
                file_path = os.path.join(warm_dir, file)
                if(os.path.isdir(file_path)):
                    if(path == '/'):
                        do_warmup(file_path, warm_cnt, path + file)
                    else:
                        do_warmup(file_path,
                                  warm_cnt, path + '/' + file)
                else:
                    if(path not in self.graph_map.keys()):
                        print(
                            '[WARMUP_WARN] path: %s not in subservices\' path, please check warm up data!' % path)
                        continue
                    if(os.path.splitext(file)[-1] == '.bin'):
                        print('[INFO] binary warmup file for %s : ' %
                              path + file)
                        with open(file_path, 'rb') as wm:
                            content = wm.read()
                            for i in range(warm_cnt):
                                t = threading.Thread(target=self.media_service.warmup, args=(
                                    self.graph_map[path].media_graph, content,))
                                warmup_pool.append(t)
                                time.sleep(0.2)
                    else:
                        print(
                            '[INFO] multi str in warmup file for %s using : ' % path + file)
                        for i in range(warm_cnt):
                            with open(file_path, 'r') as wm:
                                lines = wm.readlines()
                            for line in lines:
                                t = threading.Thread(target=self.media_service.warmup, args=(
                                    self.graph_map[path].media_graph, line,))
                                warmup_pool.append(t)
            print('[INFO] searched warmup files in the dir: warm_up' + path)

        warm_dir = self.workspace + 'warm_up'
        warmup_pool = []
        if os.path.exists(warm_dir) and os.listdir(warm_dir):
            print('[INFO] --- start warming up')
            try:
                do_warmup(warm_dir,
                          int(self.prop.get('rpc.warm_up_count', '5')))
            except Exception as e:
                print('[WARMUP_WARN] ', e)
            width = 30
            percent = 0
            alive_pool = []
            print('[INFO] warmming up, progress: [', '#' * 0, ' ' * width, ']',
                  f' {percent:.0f}%', sep='')
            for i, t in enumerate(warmup_pool):
                t.start()
                alive_pool.append(t)
                percent = float(i+1) / len(warmup_pool) * 100
                if percent % 1 <= 0.01:
                    for alive_t in alive_pool:
                        alive_t.join()
                        alive_pool.remove(alive_t)
                    left = int(width * percent / 100)
                    right = width - left
                    print('[INFO] warmming up, progress: [', '#' * left, ' ' * right, ']',
                          f' {percent:.0f}%', sep='')
            print('[INFO] --- warm up done!')
        else:
            print("[INFO] no warmup data")

    def enable_helper(self, plugin):
        self.media_service.enable_helper(plugin)

    def enable_default_helper(self):
        self.media_service.enable_helper(HELPER_CTRLSOCKET)
        self.media_service.enable_helper(HELPER_VIPSERVER)
        self.media_service.enable_helper(HELPER_LUA)
        self.media_service.enable_helper(HELPER_MIRROR)
        self.media_service.enable_helper(HELPER_SIGNALHANDLER)
        self.media_service.enable_helper(HELPER_PLUGIN)

    def enable_health_check(self):
        """
            url: http://x.x.x.x:yy/health_check
        """
        self.media_service.enable_helper(HELPER_HEALTH)

    def enable_counter(self):
        self.media_service.enable_helper(HELPER_COUNTER)

    def start_service(self):
        # warm up the service
        self.warmup()

        # enable plugins
        self.enable_default_helper()
        self.enable_health_check()
        self.enable_counter()

        # start service
        self.start()

        # set servivce ready and blocking to wait
        self.ready_to_wait()


class GraphBuilder():
    graph_builder = None

    @abstractmethod
    def run_option(self):
        return {}

    @abstractmethod
    def build_graph(self):
        raise Exception('interface build_graph must be implemented.')

    @staticmethod
    def register(build):
        GraphBuilder.graph_builder = build()

    @staticmethod
    def get_builder():
        if not GraphBuilder.graph_builder:
            raise Exception(
                'need to implement a graph builder and register it.')

        return GraphBuilder.graph_builder


# TODO: implemented with cpp while refactoring using pybind11
def load_library_op(lib, entry_class):
    def generate_op_config(args={}):
        config = {
            'name': entry_class,
            'lib_path': lib,
            'entry_class': entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config
    return generate_op_config


def cflags():
    """ get cflags for compilling a C extension
    """
    pkg_file = pkg_resources.resource_filename(__name__, "__init__.py")
    pkg_path = os.path.join(os.path.dirname(pkg_file), 'include')
    return "-I%s -D_GLIBCXX_USE_CXX11_ABI=0" % pkg_path


def ldflags():
    """ get ldflags for compilling a C extension
    """
    pkg_file = pkg_resources.resource_filename(__name__, "__init__.py")
    pkg_path = os.path.dirname(pkg_file)
    return "-L%s -lmediaflow" % pkg_path


def include_directory():
    """ get include directory for finding header files
    """
    pkg_file = pkg_resources.resource_filename(__name__, "__init__.py")
    pkg_path = os.path.join(os.path.dirname(pkg_file), 'include')
    return pkg_path


def library_path():
    """ get library path for linking
    """
    pkg_file = pkg_resources.resource_filename(__name__, "__init__.py")
    pkg_path = os.path.dirname(pkg_file)
    return '%s/libmediaflow.so' % pkg_path
