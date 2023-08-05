class window_policy:
    @staticmethod
    def select_all_window():
        config = {'window_type': 'select_all'}
        return config

    @staticmethod
    def count_window(window_count, slide_count=0):
        config = {
            'window_type': 'count_window',
            'window_count': str(window_count),
            'slide_count': str(slide_count)
        }
        return config

    @staticmethod
    def time_window(window_time, slide_time=0):
        config = {
            'window_type': 'time_window',
            'window_time': str(window_time),
            'slide_time': str(slide_time)
        }
        return config
