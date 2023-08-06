import os
import os.path
import subprocess
import sys
import sqlite3
import sys
from PySide2.QtCore import QObject, Signal, Slot, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
# from imdb import Cinemagoer
from .model.movie import Movie;
from .model.custom_models import PersonModel


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = PersonModel()
SUGGESTIONS = PersonModel()

# ia = Cinemagoer()


def db_drop(database):
    """Query DB"""
    cursor = database.cursor()
    cursor.execute("DROP TABLE movies")

def db_query(database, sql):
    """Query DB"""
    cursor = database.cursor()
    cursor.execute(sql)


def db_read(database, query):
    """Read Movies from DB"""
    try:
        cursor = database.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    except sqlite3.Error as err:
        print("Error reading data from MySQL table", err)
        return None


def db_insert(database, val):
    """Insert val in DB """


    sql = """INSERT INTO movies
                          (id, title, year, overview, genres, runtime, popularity, vote, vote_imdb, imdb_id, stars, stars_poster, char_name, poster, backdrop_path, trailer, file_name, folder, path, similarity) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    cursor = database.cursor()
    try:
        # Execute the SQL command
        cursor.execute("CREATE TABLE IF NOT EXISTS MOVIES  (id, title, year, overview, genres, runtime, popularity, vote, vote_imdb, imdb_id, stars, stars_poster, char_name, poster, backdrop_path, trailer, file_name, folder, path, similarity);")
        cursor.execute(sql, val)
        database.commit()
    except sqlite3.Error as err:
        print('Error Inserting in DB', err)
        database.rollback()
        print(err)


def db_connection():
    """Connect to DB"""
    try:
        return sqlite3.connect('myDB.db')

    except sqlite3.Error as err:
        print('Connection', 'Failed To Connect Database')
        print(err)
        sys.exit(1)


def populate_suggestions(database):
    """Populates Suggestions in main page"""
    SUGGESTIONS.clearAll()
    limit = "20"
    movies = db_read(database, 
        "SELECT * FROM movies WHERE backdrop_path NOT LIKE 'null' ORDER BY RANDOM() LIMIT " + limit)
    count = 0
    for row in movies:
        if count < 20:
            count += 1
            #                                   1   2       3       13      7       5       4       10      11          12          15           14
            #                addPerson(self, title, year, overview, poster, vote, runtime, genre, stars, starsPoster, characters, trailer, backdrop_path)
            SUGGESTIONS.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11],
                                  row[12], row[15], row[14], row[18])


def populate_movies(database, limit):
    """Gets movies in random order"""
    MODEL.clearAll()
    query = ''
    if limit == 0:
        query = "SELECT * FROM movies ORDER BY RANDOM()"
    else:
        query = "SELECT * FROM movies ORDER BY RANDOM() LIMIT " + str(limit)
    movies = db_read(database, query)
    for row in movies:
        MODEL.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11], row[12], row[15],
                        row[14], row[18])


# def background_worker(database):
#     mov = db_read(database, 'SELECT IMDBID FROM movies WHERE vote_imdb = ""')
#     for m in mov:
#         imdb_id = m[0].replace('tt', '')
#         rating = ia.get_movie(imdb_id).get('rating')
#         sql = "UPDATE movies SET vote_imdb = '" + \
#             str(rating) + "' WHERE vote_imdb = ''"
#         print('BACKGROUND RATING ' + str(rating))
#         print('BACKGROUND id ' + str(imdb_id))
#         db_read(database, sql)


def get_length(filename):
    result = subprocess.run(['cmd.exe', '/c', 'ffprobe', '-v', 'error',
                             '-show_entries', 'format=duration', '-of',
                             'default=noprint_wrappers=1:nokey=1', '-sexagesimal',
                             filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    duration = str(result.stdout.decode("utf-8")).split(':')
    dur = int(duration[0]) * 60 + int(duration[1])
    print(str(dur) + ' min')
    return dur


def folder_name(path, number):
    """This module does blah blah."""

    return path.split('\\')[-number]


class MyApp(QObject):
    movie = Signal(str)
    poster = Signal(str)
    clearMovies = Signal()
    closeFilter = Signal(str)
    movies = []
    scrap = ''
    database = None

    @Slot(str)
    def submit_filter(self, query):
        """Filter database with the provided query"""

        query = query.split('|')
        text = query[2].replace(' OR', ',').replace(' AND', ',') + ':'
        if text == ':':
            text = "Random Movies:"
        query[0] = query[0].replace('Year >=', 'year BETWEEN').replace('Year <=','')
        query[1] = query[1].replace('Rating >=', 'vote BETWEEN').replace('Rating <=','')
        query[3] = query[3].replace('Sort By:', 'ORDER BY').replace(
            'Name', '`title` ASC').replace('Year', '`year` DESC').replace('Vote', '`vote` DESC')
        query[2] = query[2].replace('Action', "`genres` LIKE '%Action%'") \
            .replace('Animation', "`genres` LIKE '%Animation%'") \
            .replace('Adventure', "`genres` LIKE '%Adventure%'") \
            .replace('Comedy', "`genres` LIKE '%Comedy%'") \
            .replace('Crime', "`genres` LIKE '%Crime%'") \
            .replace('Documentary', "`genres` LIKE '%Documentary%'") \
            .replace('Drama', "`genres` LIKE '%Drama%'") \
            .replace('Family', "`genres` LIKE '%Family%'") \
            .replace('Fantasy', "`genres` LIKE '%Fantasy%'") \
            .replace('History', "`genres` LIKE '%History%'") \
            .replace('Horror', "`genres` LIKE '%Horror%'") \
            .replace('Music', "`genres` LIKE '%Music%'") \
            .replace('Mystery', "`genres` LIKE '%Mystery%'") \
            .replace('Romance', "`genres` LIKE '%Romance%'") \
            .replace('Science Fiction', "`genres` LIKE '%Science Fiction%'") \
            .replace('TV Movie', "`genres` LIKE '%TV Movie%'") \
            .replace('Thriller', "`genres` LIKE '%Thriller%'") \
            .replace('War', "`genres` LIKE '%War%'") \
            .replace('Western', "`genres` LIKE '%Western%'")

        print('REFORM')
        base_query = 'SELECT * FROM movies WHERE '
        parameters = ''
        for param in query:
            if len(param) >= 1:
                parameters += '' + param + ' AND '
        query = base_query + parameters[:-5].replace('AND ORDER', 'ORDER') \
            .replace(' ASC)', ' ASC') \
            .replace(' DESC)', ' DESC')
        mov = db_read(self.database, query)
        MODEL.clearAll()
        self.closeFilter.emit(text)
        for row in mov:
            MODEL.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11], row[12], row[15],
                            row[14], row[18])

    @Slot(str)
    def onSearch(self, search):
        """Searches database for @search"""
        print('Searching for ' + search)
        query = ''
        query = "SELECT * FROM movies WHERE `title` LIKE '%" + search + \
            "%' OR `stars` LIKE '%" + search + "%' ORDER BY title "
        print(query)
        movies = db_read(query)
        MODEL.clearAll()
        for row in movies:
            MODEL.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11], row[12], row[15],
                            row[14], row[18])

    @Slot(str)
    def onClick(self):
        print('click')

    @Slot(str)
    def watch(self, path):
        """Starts movie from path"""
        p = 'cmd /c "start "" "' + path
        p += '"'
        os.system(p)

    @Slot(str)
    def onComp(self, str):
        """Main GUI init"""

        if str == 'Home':
            populate_suggestions(self.database)
            populate_movies(self.database, 21)
        elif str == 'Main':
            populate_movies(self.database, 0)

    def db_init(self, database, path):
        """Init DB"""
        try:
            db_drop(database)
        finally:
            count = 0
            for root, dirs, files in os.walk(path):
                for file in files:
                    if (file.endswith(".VOB") or file.endswith(".avi") or
                            file.endswith(".mp4") or file.endswith(".mkv")):
                        path = os.path.join(root, file)
                        if file.endswith(".VOB"):
                            # 3 .vob #2 all
                            folder = folder_name(path, 3)
                            filename = folder
                        else:
                            folder = folder_name(path, 2)
                            filename = file
                        if count <= 1000000:
                            print('------')
                            path = os.path.join(root, file)

                            print('p: ' + path)
                            if 'CD2' not in filename and 'cd2' not in filename:
                                movie = Movie(True, (filename, folder, path))
                                if movie.scrap != '' and movie.scrap:
                                    ts = movie.scrap.split(', ')
                                    for scrapi in ts:
                                        if scrapi not in self.scrap.split(', '):
                                            self.scrap += movie.scrap
                                print(str(count))

                                entry = movie.get_db_entry()
                                db_insert(database, entry)
                                self.movies.append(movie)

                        count += 1

    @Slot()
    def exit(self):
        sys.exit(-1)

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.database = db_connection()


        try:
            path = sys.argv[1]
            self.db_init(self.database, path)
        except BaseException  as error:
            mov = db_read(self.database, 'SELECT * FROM `movies`')
            if(mov != None):
                for row in mov:
                    self.movies.append(Movie(False, row))
            else:          
                print('Database is Empty')
                sys.exit(-1)


def run():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    main = MyApp()
    engine.rootContext().setContextProperty('myListModel', MODEL)
    engine.rootContext().setContextProperty('SuggestionsModel', SUGGESTIONS)
    engine.rootContext().setContextProperty("MyApp", main)
    engine.load(QUrl.fromLocalFile(
        os.path.join(CURRENT_DIR, 'qt/mainWindow.qml')))
    # engine.load(QUrl.fromLocalFile(
    #     os.path.join('..\qt\mainWindow.qml')))
    # print(os.path.join(CURRENT_DIR, 'qt/mainWindow.qml'))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
    