class Log(object):
    def __init__(self, log_type, date, thread_id, filename, line_num, log_msg):
        self.log_type = log_type
        self.date = date
        self.thread_id = int(thread_id)
        self.filename = filename
        self.line_num = int(line_num)
        self.log_msg = log_msg
