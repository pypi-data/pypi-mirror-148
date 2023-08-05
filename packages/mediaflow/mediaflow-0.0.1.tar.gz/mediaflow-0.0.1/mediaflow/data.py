from ast import arguments
from . import get_default_graph
from . import config

import copy


def create_op(op_type, function, op_config, args):
    if function is not None:
        atrrs = dir(function)
        if '__call__' in atrrs:
            # c++/python decorator
            config = function()

            # default is c++ operator
            if 'language' not in config:
                config['language'] = 'cpp'
        else:
            # python class
            entry_class = function.__module__ + "." + function.__name__
            config = {
                'name': function.__name__,
                'language': 'python',
                'entry_class': entry_class
            }

        op_config.update(config)

        if 'name' not in config:
            raise Exception('Exception: this node does not has name!')

    op_config['op_type'] = 'Python' + \
                           op_type if op_config['language'] == 'python' else op_type

    # TODO __arguments__ contains the default arguments, move into op's implemention
    arguments = {}
    if '__arguments__' in op_config:
        arguments = op_config['__arguments__']
        del op_config['__arguments__']

    arguments.update(args)

    node_name = op_config['name'] + "_" + get_default_graph().get_id(function)
    get_default_graph().create_op(node_name, op_config, arguments)
    return node_name


def node_create_wrapper(self, op_type, function, op_config, args):
    node_name = create_op(op_type, function, op_config, args)
    if self._is_input_:
        get_default_graph().add_op_input(node_name, self._last_op_name_)
        self._is_input_ = False
    else:
        source = self._last_op_name_ + ':' + str(self._output_)
        get_default_graph().connect_op(source, node_name)
    self._last_op_name_ = node_name
    self.clear()

    return self


class DataFrames:
    def __init__(self, name, is_input=True):
        self._last_op_name_ = name
        self._output_ = 0
        self._is_input_ = is_input
        if is_input:
            get_default_graph().create_input(name)

    def map(self, function, op_config={}, args={}):
        return node_create_wrapper(self, 'MapOp', function, op_config, args)

    def stream_map(self, function, op_config={}, args={}):
        return node_create_wrapper(self, 'StreamMapOp', function, op_config, args)

    def process(self, args):
        op_type = args['op_type']
        op_config = {
            'name': args['name'],
            'language': 'cpp'
        }
        return node_create_wrapper(self, op_type, None, op_config, args)

    # for >> operator
    def __rshift__(self, other):
        return self.map(other)

    def flat_map(self, function, op_config={}, args={}):
        return node_create_wrapper(self, 'FlatMapOp', function, op_config, args)

    def filter(self, function, op_config={}, args={}):
        return node_create_wrapper(self, 'FilterOp', function, op_config, args)

    def window(self, window_policy, function, args={}):
        return node_create_wrapper(self, 'WindowOp', function, window_policy, args)

    def sort_union(self, *image_frames):
        sort_union_index = get_default_graph().get_sort_union_id()
        node_name = "sort_union_" + sort_union_index
        get_default_graph().create_op(
            node_name, {'op_type': 'SortUnionOp', 'stateful': 'true'}, {})
        source = self._last_op_name_ + ":" + str(self._output_)
        dest = node_name + ":0"
        get_default_graph().connect_op(source, dest)

        output_id = 1
        if isinstance(image_frames[0], list):
            image_frames = image_frames[0]
        for data_frame in image_frames:
            self._output_ += 1
            source = data_frame._last_op_name_ + ":" + str(data_frame._output_)
            dest = node_name + ":" + str(output_id)
            get_default_graph().connect_op(source, dest)
            data_frame.clear()
            output_id += 1

        self._last_op_name_ = node_name
        self.clear()
        return self

    def merge(self, *image_frames):
        merge_index = get_default_graph().get_merge_id()
        node_name = "merge_" + merge_index
        get_default_graph().create_op(
            node_name, op_config={'op_type': 'MergeOp', "stateful": "true"})
        source = self._last_op_name_ + ":" + str(self._output_)
        dest = node_name + ":0"
        get_default_graph().connect_op(source, dest)

        output_id = 1
        if isinstance(image_frames[0], list):
            image_frames = image_frames[0]
        for data_frame in image_frames:
            self._output_ += 1
            source = data_frame._last_op_name_ + ":" + str(data_frame._output_)
            dest = node_name + ":" + str(output_id)
            get_default_graph().connect_op(source, dest)
            data_frame.clear()
            output_id += 1

        self._last_op_name_ = node_name
        self.clear()
        return self

    def merge_sequential(self, *image_frames):
        merge_sequential_index = get_default_graph().get_merge_sequential_id()
        node_name = "merge_sequential_" + merge_sequential_index
        get_default_graph().create_op(
            node_name, op_config={'op_type': 'MergeSequentialOp', "stateful": "true"})
        source = self._last_op_name_ + ":" + str(self._output_)
        dest = node_name + ":0"
        get_default_graph().connect_op(source, dest)

        output_id = 1
        if isinstance(image_frames[0], list):
            image_frames = image_frames[0]
        for data_frame in image_frames:
            self._output_ += 1
            source = data_frame._last_op_name_ + ":" + str(data_frame._output_)
            dest = node_name + ":" + str(output_id)
            get_default_graph().connect_op(source, dest)
            data_frame.clear()
            output_id += 1

        self._last_op_name_ = node_name
        self.clear()
        return self

    def route(self, function, outputs, op_config={}, args={}):
        node_name = create_op('RouteOp', function, op_config, args)
        get_default_graph().connect_op(self._last_op_name_, node_name)

        frames = []
        self._last_op_name_ = node_name
        self._output_ = 0
        frames.append(self)
        for idx in range(1, outputs):
            new_output = copy.copy(self)
            new_output._last_op_name_ = node_name
            new_output._output_ = idx
            frames.append(new_output)
        return tuple(frames)

    def stream_read(self, function, op_config={}, args={}):
        op_config["stateful"] = "true"
        return node_create_wrapper(self, 'StreamReadOp', function, op_config, args)

    def stream_write(self, function, op_config={}, args={}):
        op_config["stateful"] = "true"
        return node_create_wrapper(self, 'StreamWriteOp', function, op_config, args)

    def copy(self):
        new_image_frames = copy.copy(self)
        # new_image_frames.output = 0   self.ref['value']
        # self.ref['value'] += 1
        return new_image_frames

    def last(self, op_config={}, args={}):
        config = {
            'op_type': 'LastOp',
            'stateful': 'true'
        }
        config.update(op_config)
        last_id = get_default_graph().get_last_id()
        node_name = "last_" + last_id
        get_default_graph().create_op(node_name, config, args)
        source = self._last_op_name_ + ":" + str(self._output_)
        dest = node_name + ":0"
        get_default_graph().connect_op(source, dest)

        self._last_op_name_ = node_name
        self.clear()
        return self

    def scan(self, function, op_config={}, args={}):
        op_config["stateful"] = "true"
        return node_create_wrapper(self, 'ScanOp', function, op_config, args)

    def concat_with(self, function, op_config={}, args={}):
        return node_create_wrapper(self, 'ConcatWithOp', function, op_config, args)

    def splitby(self, function, args={}, subgraph=None):
        if not node_create_wrapper(self, 'SplitOp', function, {}, args):
            return
        if not subgraph:
            return

        id = get_default_graph().get_id('split_graph')
        graph_name = 'split_graph_' + str(id)
        get_default_graph().add_subgraph(graph_name, subgraph)
        source = self._last_op_name_ + ":" + str(self._output_)
        dest = graph_name + ":0"
        get_default_graph().connect_op(source, dest)
        self._last_op_name_ = graph_name
        return self

    def output(self, name):
        get_default_graph().add_op_output(self._last_op_name_, name)

    def clear(self):
        self._output_ = 0


class ImageFrames(DataFrames):
    def __init__(self, name, is_input=True):
        DataFrames.__init__(self, name, is_input)


class AudioFrames(DataFrames):
    def __init__(self, name, is_input=True):
        DataFrames.__init__(self, name, is_input)


class MediaData(DataFrames):
    def __init__(self, name, is_input=True):
        DataFrames.__init__(self, name, is_input)


class Video:
    def __init__(self, name, is_input=True):
        self._last_op_name_ = name
        self._output_ = 0
        self._is_input_ = is_input
        if is_input:
            get_default_graph().create_input(name)

    def decode_image(self, decode_config={}):
        import mediaflow_ops_codec as codec

        decode_image_index = get_default_graph().get_decode_image_id()
        op_name = "image_decoder_" + decode_image_index

        decode_config['type'] = 'image'
        if 'use_gpu' not in decode_config:
            decode_config['use_gpu'] = str(False)

        op_config = codec.decoder({'use_gpu': decode_config['use_gpu'].lower() == 'true'})

        get_default_graph().create_op(op_name, op_config, decode_config)
        if self._is_input_:
            get_default_graph().add_op_input(op_name, self._last_op_name_)
            self._is_input_ = False
        else:
            get_default_graph().connect_op(self._last_op_name_ + ":0", op_name + ":0")
        self._last_op_name_ = op_name
        return ImageFrames(self._last_op_name_, False)

    def decode_audio(self, decode_config={}):
        import mediaflow_ops_codec as codec

        decode_audio_index = get_default_graph().get_decode_audio_id()
        op_name = "audio_decoder_" + decode_audio_index

        decode_config['type'] = 'audio'
        if 'use_gpu' not in decode_config:
            decode_config['use_gpu'] = str(False)

        op_config = codec.decoder({'use_gpu': decode_config['use_gpu'].lower() == 'true'})

        get_default_graph().create_op(op_name, op_config, decode_config)
        if self._is_input_:
            get_default_graph().add_op_input(op_name, self._last_op_name_)
            self._is_input_ = False
        else:
            get_default_graph().connect_op(self._last_op_name_ + ':0', op_name + ":0")
        self._last_op_name_ = op_name
        return AudioFrames(self._last_op_name_, False)

    def decode(self, decode_config={}):
        import mediaflow_ops_codec as codec

        decode_image_audio_index = get_default_graph().get_decode_image_audio_id()
        op_name = "decoder_" + decode_image_audio_index

        decode_config['type'] = 'image_audio'
        if 'use_gpu' not in decode_config:
            decode_config['use_gpu'] = str(False)

        op_config = codec.decoder({'use_gpu': decode_config['use_gpu'].lower() == 'true'})

        get_default_graph().create_op(op_name, op_config, decode_config)
        if self._is_input_:
            get_default_graph().add_op_input(op_name, self._last_op_name_)
            self._is_input_ = False
        else:
            get_default_graph().connect_op(self._last_op_name_ + ":" + str(0),
                                           'decode_image_audio_' + decode_image_audio_index + ":0")
        self._last_op_name_ = op_name

        op_name = 'ImageAudioSeparater_' + \
                  get_default_graph().get_image_audio_seprate_id()

        op_config = codec.image_audio_separater()
        get_default_graph().create_op(op_name, op_config, {})
        get_default_graph().connect_op(self._last_op_name_, op_name)

        image_frames = ImageFrames(op_name, False)
        image_frames._output_ = 0
        audio_frames = AudioFrames(op_name, False)
        audio_frames._output_ = 1

        return image_frames, audio_frames

    @staticmethod
    def encode(image_frames, audio_frames=None, encode_config={}):
        import mediaflow_ops_codec as codec

        graph = get_default_graph()
        op_name = "encoder_" + str(graph.get_encode_id())

        encode_config['in_memory'] = 'true'
        if 'use_gpu' not in encode_config:
            encode_config['use_gpu'] = str(False)

        op_config = codec.encoder({'use_gpu': encode_config['use_gpu'].lower() == 'true'})

        graph.create_op(op_name, op_config, encode_config)

        video = Video(op_name, False)
        video._last_op_name_ = op_name

        source = image_frames._last_op_name_ + ":" + str(image_frames._output_)
        dest = op_name + ":0"
        graph.connect_op(source, dest)
        image_frames._output_ = 0

        if audio_frames:
            source = audio_frames._last_op_name_ + \
                     ":" + str(audio_frames._output_)
            dest = op_name + ":1"
            graph.connect_op(source, dest)
            audio_frames._output_ = 0

        return video

    def clear(self):
        self._output_ = 0

    def map(self, function, args={}):
        return node_create_wrapper(self, 'MapOp', function, '', args)
