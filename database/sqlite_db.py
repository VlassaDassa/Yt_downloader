import sqlite3

class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    async def set_status_download(self, tgid, status):
        with self.connection:
            self.cursor.execute('INSERT OR IGNORE INTO `status_download`(`tgid`, `status`) VALUES (?, ?)', (tgid, status, ))


    async def get_status_download(self, tgid):
        with self.connection:
            return self.cursor.execute('SELECT `status` FROM `status_download` WHERE tgid=?', (tgid, )).fetchone()


    async def update_status_download(self, tgid, status):
        with self.connection:
            self.cursor.execute('UPDATE `status_download` SET status=? WHERE tgid=?', (status, tgid, ))


    async def add_file(self, tgid, count):
        with self.connection:
            self.cursor.execute('INSERT OR IGNORE INTO `count_file`(`tgid`, `count`) VALUES (?, ?)', (tgid, count, ))


    async def get_count_file(self, tgid):
        with self.connection:
            return self.cursor.execute('SELECT `count` FROM `count_file` WHERE tgid=?', (tgid, )).fetchone()


    async def update_count_file(self, tgid, count):
        with self.connection:
            self.cursor.execute('UPDATE `count_file` SET count=? WHERE tgid=?', (count, tgid, ))


# count_file
# - count
# - tgid

# status_download
# - tgid
# - status