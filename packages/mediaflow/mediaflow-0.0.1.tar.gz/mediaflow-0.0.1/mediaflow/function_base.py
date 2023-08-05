# encoding=utf-8


class FunctionBase(object):
    def __init__(self):
        pass

    def init(self, parameter):
        return True

    def clean(self):
        pass

    pass


class MapFunction(FunctionBase):
    def map(self, data_frame, context):
        pass


class FlatMapFunction(FunctionBase):
    def flat_map(self, data_frame, context):
        return list()


class FilterFunction(FunctionBase):
    def filter(self, data_frame, context):
        return False


class WindowFunction(FunctionBase):
    def window(self, data_frame_list_input, context):
        return list()


class RouteFunction(FunctionBase):
    def route(self, data_frame, context):
        return 0


class StreamReadFunction(FunctionBase):
    def open(self, source_data, context):
        pass

    def read(self, context):
        return False

    def close(self, context):
        pass


class StreamWriteFunction(FunctionBase):
    def open(self, context):
        pass

    def write(self, data_frame, context):
        return False

    def close(self, context):
        pass


class ScanFunction(FunctionBase):
    def scan(self, pre_data_frame, data_frame, context):
        pass


class ConcatWithFunction(FunctionBase):
    def concat_with(self, context):
        return list()


# split interface which could cut stream to some substreams
# if split return True, the stream will be cutted.
class SplitFunction(FunctionBase):
    def split(self, data_frame, context):
        return False
