from time import gmtime, strftime

class Code:
    
    @staticmethod
    def uniquecode():
        showtime = strftime("%Y%m%d%H%M%S", gmtime())
        return showtime
