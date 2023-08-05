from .function_base import MapFunction, FlatMapFunction, FilterFunction, SplitFunction, WindowFunction, RouteFunction, ScanFunction, ConcatWithFunction


class map(MapFunction):
    def __init__(self, map_func):
        self._func = map_func
        m = map_func.__globals__['__name__']
        self.entry_class = m + "." + map_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def map(self, data_frame, context):
        self._func(data_frame, context)


class filter(FilterFunction):
    def __init__(self, filter_func):
        self._func = filter_func
        m = filter_func.__globals__['__name__']
        self.entry_class = m + "." + filter_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def filter(self, data_frame, context):
        return self._func(data_frame, context)


class flat_map(FlatMapFunction):
    def __init__(self, flat_map_func):
        self._func = flat_map_func
        m = flat_map_func.__globals__['__name__']
        self.entry_class = m + "." + flat_map_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def flat_map(self, data_frame, context):
        return self._func(data_frame, context)


class window(WindowFunction):
    def __init__(self, window_func):
        self._func = window_func
        m = window_func.__globals__['__name__']
        self.entry_class = m + "." + window_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def window(self, data_frame_list_input, context):
        return self._func(data_frame_list_input, context)


class route(RouteFunction):
    def __init__(self, route_func):
        self._func = route_func
        m = route_func.__globals__['__name__']
        self.entry_class = m + "." + route_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def route(self, data_frame, context):
        return self._func(data_frame, context)


class scan(ScanFunction):
    def __init__(self, scan_func):
        self._func = scan_func
        m = scan_func.__globals__['__name__']
        self.entry_class = m + "." + scan_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def scan(self, pre_data_frame, data_frame, context):
        self._func(pre_data_frame, data_frame, context)


class concat_with(ConcatWithFunction):
    def __init__(self, concat_with_func):
        self._func = concat_with_func
        m = concat_with_func.__globals__['__name__']
        self.entry_class = m + "." + concat_with_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def concat_with(self, context):
        return self._func(context)


class split(SplitFunction):
    def __init__(self, split_func):
        self._func = split_func
        m = split_func.__globals__['__name__']
        self.entry_class = m + "." + split_func.__name__

    def __call__(self, args={}):
        config = {
            'name': self._func.__name__,
            'language': 'python',
            'entry_class': self.entry_class,
            '__arguments__': {}
        }
        config['__arguments__'].update(args)
        return config

    def split(self, dataframe, context):
        return self._func(dataframe, context)
