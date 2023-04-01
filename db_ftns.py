import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()


# Creating Table
def create_uploadfile_table():
    # c.execute("DROP TABLE filestable")
    c.execute(
        "CREATE TABLE IF NOT EXISTS filestable(filename TEXT,filetpe TEXT,filesize TEXT,UploadTime TIMESTAMP)"
    )


def add_file_details(filename, filetype, filesize, UploadTime):
    c.execute(
        "INSERT INTO filestable(filename,filetpe,filesize,UploadTime) VALUES(?,?,?,?)",
        (filename, filetype, filesize, UploadTime),
    )
    conn.commit()


def view_all_data():
    c.execute("SELECT * FROM filestable")
    data = c.fetchall()
    return data
