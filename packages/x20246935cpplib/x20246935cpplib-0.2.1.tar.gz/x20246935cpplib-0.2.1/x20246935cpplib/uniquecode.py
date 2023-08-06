from time import gmtime, strftime

class Code:
    
    def uniquecode(self):
        showtime = strftime("%Y%m%d%H%M%S", gmtime())
        return showtime
