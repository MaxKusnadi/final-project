
class Utils:

    @staticmethod
    def create_error_code(error, *args):
        d = error
        d['text'] = d['text'].format(args)
        return d