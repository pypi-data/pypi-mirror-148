import re
from tmdbv3api import TMDb
import requests
import os
from pyjarowinkler import distance
import Levenshtein
import shutil
from imdb import IMDb

from .cast import Cast

ia = IMDb()
tmdb = TMDb()
tmdb.debug = True
tmdb.api_key = '03417c8113bb7602f27eed0cf17f86e7'


class Movie:

    id = ''
    title = ''
    year = 0
    json = ''
    overview = ''
    genres = ''
    runtime = ''
    vote = 0.0
    popularity = ''
    vote_imdb = ''
    imdb_id = ''
    stars = ''
    stars_poster = ''
    character = ''
    poster = ''
    backdrop_path = ''
    trailer = ''
    file_name = ''
    folder = ''
    credit = []
    path = ''
    similarity = 0
    scrap = ''

    def get_db_entry(self):
        """This module does blah blah."""
        return (self.id,
                self.title,
                self.year,
                self.overview,
                self.genres,
                self.runtime,
                self.popularity,
                self.vote,
                self.vote_imdb,
                self.imdb_id,
                self.stars,
                self.stars_poster,
                self.character,
                self.poster,
                self.backdrop_path,
                self.trailer,
                self.file_name,
                self.folder,
                self.path,
                self.similarity
                )

    def levenshtein_similarity(self, a, b):
        """Get Levenshtein Similarity"""
        max_len = max(len(a), len(b))
        dis = Levenshtein.distance(a, b)
        score = abs(max_len - dis) * 100 / max_len
        return score

    def jarow_similarity(self, a, b):
        """Get Jarow Similarity"""
        score = distance.get_jaro_distance(a, b, winkler=True, scaling=0.1) * 100
        return score

    def score(self, a, b):
        """Combine the two similarity methods to get score"""
        score = self.levenshtein_similarity(a, b) + self.jarow_similarity(a, b)
        return score

    def similar(self, a, b):
        return Levenshtein.distance(a.lower(), b.lower())

    def search_movie_json(self, name, year, folder, similarity):
        """Search for movie in API DB and get json"""
        name = name.replace('&', 'and').replace(':', ' ').lower().strip()
        if name[-2:] == ' 1': name = name.replace(' 1', '')
        og_name = name
        results = ('', '', '', similarity)
        if year == 'null':
            year = ''

        filename = [name, '']

        count_split = 0
        continue_while = True
        triggered = False

        while len(filename) > 1 and continue_while:
            json = self.query_movie(filename[0], year)

            if filename[0][-1] == ' ':
                filename[0] = filename[0][:-1]
            if json['total_results'] != 0:
                if triggered == False:
                    name = filename[0]
                    triggered = True

                i = 0
                for i in range(len(json['results'])):
                    if i <= 10:
                        r = json['results'][i]
                        max_score = 200 + 50 + 20 - 10
                        if ('release_date' in r and r['release_date'] != "" and r['vote_count'] > 0):
                            r_id = r['id']
                            r_name = r['title'].replace('&', 'and').replace('-', ' ').replace('⅓', '').replace('½', '')

                            if any(x in r_name.rsplit(' ', 1) for x in
                                   [' ii', ' iii', ' iv', 'v', ' vi', ' vii', ' viii']):
                                print('REPLACING ROMANS')
                                r_name = r_name.replace(' ii', ' 2').replace(' iii', ' 3').replace(' iv', ' 4').replace(
                                    ' v', ' 5').replace(' vi', ' 6').replace(' vii', ' 7').replace(' viii', ' 8')

                            r_name = " ".join(r_name.split())
                            r_year = r['release_date'].split('-')[0]
                            r_distance = self.score(name, r_name.lower()) - 5 * count_split - (i + 1) * (
                                    count_split + 1) * 10
                            if ':' in r_name:
                                s_name = r_name.split(':')
                                s1_distance = (self.score(name, s_name[0].lower()) - 25 * count_split - (i + 1) * (
                                        count_split + 1) * 10) * 75 / 100
                                s2_distance = self.score(name, s_name[1].lower()) - 25 * count_split - (i + 1) * (
                                        count_split + 1) * 10
                                if r_distance < s1_distance: r_distance = s1_distance
                                if r_distance < s2_distance: r_distance = s2_distance

                            if year != '' and abs(int(r_year) - int(year)) <= 1: r_distance += 50
                            if r['backdrop_path'] is not None: r_distance += 20
                            if folder == 'fOn': r_distance -= 25
                            r_distance = r_distance * 100 / max_score
                            tupple = (r_name, r_year, r_id, r_distance)

                            if results[3] < tupple[3]:
                                results = tupple
                                if results[3] == 100:
                                    self.similarity = results[3]
                                    return results[2]

            if len(filename) == 1:
                continue_while = False
            else:
                filename = filename[0].rsplit(' ', 1)
                if filename[0][-2:] == ' 1':
                    filename[0] = filename[0].replace(' 1', '')
                if triggered: count_split += 1
                if count_split == 3: continue_while = False
                if filename[0] == 'the': continue_while = False
            if len(filename) > 1 and filename[1] != '':
                self.scrap += filename[1] + ', '
            if (len(filename) == 1 or continue_while == False) and year != '':
                count_split = 0
                continue_while = True
                filename = [og_name, '']
                name = og_name
                year = ''
                triggered = False

            if (len(filename) == 1 or continue_while == False) and year == '' and folder != 'fOn':
                count_split = 0
                continue_while = True
                extraction = self.extract_name_year(folder)
                folder = extraction[0]
                year = extraction[1]
                name = folder.replace('&', 'and').replace(':', ' ').lower().strip()
                filename = [folder.replace('&', 'and').replace(':', ' ').lower().strip(), '']
                folder = 'fOn'
                triggered = False

            if len(filename) == 1 and year == '' and folder == 'fOn':
                continue_while = False
        self.similarity = results[3]
        return results[2]

    def extract_name_year(self, name):
        """Extract year from filename if it exists"""
        name = self.clear_name(name)
        year = re.sub("[^0-9]", " ", name)
        number = [int(s) for s in year.split() if s.isdigit() and len(s) == 4]
        if len(number) == 0:
            year = ''
        elif len(number) == 1:
            year = str(number[0])
            name = name.replace(year, '')
        else:
            year = str(number[len(number) - 1])
            name = name.replace(year, '')
        return (name, year)

    def query_duration(self, id):
        """Get runtime from json"""
        json = self.get_json_movie(id)
        if 'runtime' in json and json['runtime'] is not None:
            return json['runtime']
        return 0

    def query_movie(self, name, year):
        """Search movie in the API"""
        url = 'https://api.themoviedb.org/3/search/movie?api_key=' \
              + tmdb.api_key + '&query=' \
              + name
        if year != '':
            url += '&year=' + year
        response = requests.get(url)
        return response.json()

    def clear_name(self, name):
        """Clear filename"""
        name = name.replace('[', ' ') \
            .replace(']', ' ') \
            .replace('{', ' ') \
            .replace('}', ' ') \
            .replace('_', ' ') \
            .replace('(', ' ') \
            .replace(')', ' ') \
            .replace('.avi', ' ') \
            .replace('.mp4', ' ') \
            .replace(' MP3', ' ') \
            .replace('.mkv', ' ') \
            .replace('.', ' ') \
            .replace("Unrated Edition", ' ') \
            .replace("Director's Cut", ' ') \
            .replace("Ultimate Cut", ' ') \
            .replace('YIFY', ' ') \
            .replace('Extended Edition', ' ') \
            .replace('LiNE', ' ') \
            .replace('BrRip', ' ') \
            .replace('BRRIP', ' ') \
            .replace('BRrip', ' ') \
            .replace('BRRip', ' ') \
            .replace('BDrip', ' ') \
            .replace('-NeDiVx', ' ') \
            .replace('DVDrip', ' ') \
            .replace('DVDRip', ' ') \
            .replace('DVDRIP', ' ') \
            .replace('DVDRiP', ' ') \
            .replace('DvDrip', ' ') \
            .replace('DvdRip', ' ') \
            .replace('DvDRip', ' ') \
            .replace('DVDRip', ' ') \
            .replace(' Eng ', ' ') \
            .replace('DTS', ' ') \
            .replace('BluRay', ' ') \
            .replace('x264', ' ') \
            .replace('X264', ' ') \
            .replace('YTS.AG', ' ') \
            .replace('1080p', ' ') \
            .replace('720p', ' ') \
            .replace('720P', ' ') \
            .replace('HDTV', ' ') \
            .replace('H264', ' ') \
            .replace('XviK', ' ') \
            .replace('XVID', ' ') \
            .replace('DiVX', ' ') \
            .replace('XviD', ' ') \
            .replace('xvid', ' ') \
            .replace('Xvid', ' ') \
            .replace('XViD', ' ') \
            .replace('HC HDRip', ' ') \
            .replace('aXXo', ' ') \
            .replace('Jaybob', ' ') \
            .replace('iNTERNAL', ' ') \
            .replace('FLAWL3SS', ' ') \
            .replace('-Subzero', ' ') \
            .replace('MULTISUBS', ' ') \
            .replace('greenbud1969', ' ') \
            .replace('BOKUTOX', ' ') \
            .replace(' DASH ', ' ') \
            .replace('AC3', ' ') \
            .replace('AAC', ' ') \
            .replace('-DoNE', ' ') \
            .replace('-DVDSCR', ' ') \
            .replace('-RARBG', ' ') \
            .replace('-FXG ', ' ') \
            .replace('ExtraTorrentRG ', ' ') \
            .replace('Unrated Edition', ' ') \
            .replace('MAXSPEED www torentz 3xforum ro', ' ') \
            .replace('Stealthmaster ', ' ') \
            .replace('BLiTZKRiEG', ' ') \
            .replace('UNRATED', ' ') \
            .replace('MAXSPEED', ' ') \
            .replace('KLAXXON', ' ') \
            .replace('WEB-DL', ' ') \
            .replace(' TS ', ' ') \
            .replace(' GR ', ' ') \
            .replace(' gre ', ' ') \
            .replace(' DVD ', ' ') \
            .replace(' INTERNAL ', ' ') \
            .replace(' FISH ', ' ') \
            .replace('www torentz 3xforum ro', ' ') \
            .replace('CH-BLiTZCRiEG', ' ') \
            .replace(' H 2', ' ') \
            .replace(' DVDSCR www torentz 3xforum ro', ' ') \
            .replace('CD1', ' ') \
            .replace('CD2', ' ') \
            .replace(' gr ', ' ') \
            .replace(' GR ', ' ') \
            .replace(' en ', ' ') \
            .replace('1337x -Noir', ' ') \
            .replace('www.torrentday.com', ' ') \
            .replace('NikonXp', ' ') \
            .replace('READNFO ', ' ') \
            .replace(' dvd', ' ') \
            .replace('-HUBRIS', ' ') \
            .replace('-ViSiON', ' ') \
            .replace('-ZEKTORM', ' ') \
            .replace('-MEDiC', ' ') \
            .replace('-Torrents', ' ') \
            .replace('NeRoZ', ' ') \
            .replace('Greek Hard Sub -Zeus Dias', ' ') \
            .replace('-Zeus', ' ') \
            .replace('Dias', ' ') \
            .replace('-ART3MiS', ' ') \
            .replace('-FTW', ' ') \
            .replace('-DUQA', ' ') \
            .replace('-eXtasy', ' ') \
            .replace('-Dash', ' ') \
            .replace('AXL33', ' ') \
            .replace(' Subs', ' ') \
            .replace(' NL ', ' ') \
            .replace(' DVDR ', ' ') \
            .replace(' D-Z0N3 ', ' ') \
            .replace(' AG ', ' ') \
            .replace(' YTS ', ' ') \
            .replace('-DiAMOND', ' ') \
            .replace('REPACK', ' ') \
            .replace('-REBORN', ' ') \
            .replace('Drama', ' ') \
            .replace('christosk89', ' ') \
            .replace('1000x424', ' ') \
            .replace('-NewArtRiot', ' ') \
            .replace('264', ' ') \
            .replace('-BDRip-H', ' ') \
            .replace('IMAGiNE', ' ') \
            .replace('ENG', ' ') \
            .replace('G2G', ' ') \
            .replace('Hive-CM8', ' ') \
            .replace('HQ', ' ') \
            .replace('-iRipper', ' ') \
            .replace('EXTENDED', ' ') \
            .replace('-kirklestat', ' ') \
            .replace('3xforum', ' ') \
            .replace('www', ' ') \
            .replace('-FxM', ' ') \
            .replace('Dino', ' ') \
            .replace('DVDSCR', ' ') \
            .replace('DiVERSiTY', ' ') \
            .replace('R5', ' ') \
            .replace('-KingBen', ' ') \
            .replace('-Fastbet99', ' ') \
            .replace('-Zox', ' ') \
            .replace('-InfraNez', ' ') \
            .replace('-SOuVLaAKI', ' ') \
            .replace('WORKPrint', ' ') \
            .replace('DvdSCR', ' ') \
            .replace('ACT-COM-6', ' ') \
            .replace('rkg', ' ') \
            .replace('dogs', ' ') \
            .replace('-ARROW', ' ') \
            .replace('GAZ', ' ') \
            .replace('-KriS', ' ') \
            .replace('Uncut', ' ') \
            .replace('BugzBunny', ' ') \
            .replace('&', 'and')

        repl = "D-Z0N3,AG,YTS,-DiAMOND,REPACK,\
            -REBORN,christosk89,1000x424,\
            -NewArtRiot,\
            264-,\
            -BDRip-H,\
            IMAGiNE,\
            ENG,\
            G2G,\
            Hive-CM8,\
            -iRipper,\
            -kirklestat,\
            3xforum,\
            FxM,\
            DVDSCR,\
            DiVERSiTY,\
            R5,\
            KingBen,\
            Fastbet99,\
            -Zox,\
            -InfraNez,\
            -SOuVLaAKI,\
            WORKPrint,\
            DvdSCR,\
            ACT-COM-6,\
             rkg,\
             -ARROW,\
             GAZ,\
             -KriS,\
             BugzBunny,\
             -dbk,\
             -ETRG,\
             SubHard,\
             MP3,\
             SFTeam,\
             ARS,\
             D5,\
             subtitles,\
             ETRG,\
             juggs,\
             bitloks,\
             SUBS-ZEUS,\
             +GR,\
             -TFE,\
             AnArchy,\
             -keltz,\
             ENG,\
             DivX,\
             BugBunny,\
             PREMIERE,\
             --DMT,\
             -DASH,\
             CrEwSaDe,\
             THADOGG,\
             DivX,DUB,\
             ENG,Jet Li,\
             ShAaNiG,6CH,+HI,THEATRICAL,\
             Anniversary Edition,-Ekolb,-LW,R5-,Acesan8s,\
             Webrip,R6,Bluray,GECKOS,BDRip,-T0XiC-iNK,DVDSCR,ASTA,\
             R5Line,R5,Unrated Edition,Extreme Edition,-DMT,-WOLViSH,\
             H264,DivX-LTT,-nsiervi,-WaLMaRT,GlowGaze,pimprg,sujaidr,\
             scOrp,IMAGiNE,X264,-FLAiTE,Greekman,subs,ENG,-miguel,GMTeam,\
             -mVs,-Stealthmaster-gre,KINGDOM,-MOViERUSH,-Rx,-SANTi,480p,-UNiQUE-gre,\
             R5,DUQA,RDQ,-PLAYNOW,-JUSTiCE,Incl,~BONIIN,Eng-Hindi,Dual-Audio,hdrip,-FiSH,\
             ®,DIVX,-3Li,ViP3R,WEBRip,R6,LEGi0N,BlueLady,FREEGREEK,subENG,audioGREEK,PEACHKIDSANIM,\
             TiMPE, PrisM,MgB,DvDRiP,Rip,AUDIO, COCAIN,KingdomRelease,iLLUSiON,\
             dubbed,GrSubs,anoXmous,mobiX,SAFCuk009,1337x,FooKaS,descargasweb,\
              1PARTiCLE,descargasweb,2PARTiCLE,600MB,PROPER,loco100,ALLiANCE,\
              WBZ,PPVRip,kragion,Greek Hard Subbed,Ac3, WS ,KiNGDOM,LoRD,\
              amiable,WunSeeDee,MultiSub,122mp3,862kbs,25fps,624x256,IGUANA,DVDRip,\
              PsyCoSys,Jim Carrey,AbSurdiTygre,CaLvIn,Ac35,bdk,KIDZCORNERandJ,BPDcarrier,Dvd,\
              FiveXS,STUDIOAUDIO,R5,JYK,amiable,bdrip,MovieTorrentz,DivXLTT,TELESYNC,Dita496,\
              1337x,Ekolb,Edition,Collectors Version,Uncut Disc,USABIT,Toxic3,EMPIrE,Dvdscr,Xanthippus,\
              UsaBit,DiVERSiTY,-juggs,aarkay,ENG+HINDI,5rFF,BoBo,Grsubs,Zuzuu,geckosa,geckosb,EngFxM,SaiyanWarrior,\
              DVDSCREDAW2013,Gabor1,Zsa,Zsa,VLiS,BDRip,RC,NORAR,TiMKY,Engsub,Bloodgre,-jimmis,keltz,-SiNNERS,-DVL,\
              Northern Movies,-JNS,-JYK,HDRip,REFiNED,-TB,woodster-gre,  Version Collectors"
        repl = repl.split(',')

        for r in repl:
            name = name.replace(r, ' ')
        name = name.replace(' -', ' ')
        name = re.sub('\\s\\s+', ' ', name)
        return name.rstrip()

    def get_json(self, name, year, folder):
        """search for json"""
        js = self.search_movie_json(name, year, folder, 1)
        return js

    def get_json_movie(self, id):
        """Get json from movie"""
        url = 'https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=' \
              + tmdb.api_key + '&language=en-US'
        response = requests.get(url)
        return response.json()

    def get_trailer(self, id):
        """get trailer link"""
        url = 'https://api.themoviedb.org/3/movie/' + str(id) + '/videos?api_key=' \
              + tmdb.api_key + '&language=en-US'
        response = requests.get(url)
        if len(response.json()["results"]) != 0:
            for i in response.json()['results']:
                if i['type'] == 'Trailer':
                    return i['key']
            return response.json()['results'][0]['key']
        else:
            return 'null'

    def get_credits(self, id):
        """returns credits"""
        url = 'https://api.themoviedb.org/3/movie/' + str(id) + '/credits?api_key=' + tmdb.api_key
        response = requests.get(url)
        cast = response.json()['cast']

        for c in cast:
            ca = Cast(c)
            self.stars += ca.name + ', '
            self.stars_poster += ca.profile_path + ', '
            self.character += ca.character + ', '

        if len(self.stars) != 0:
            self.stars = self.stars[:-2]
            self.character = self.character[:-2]
            self.stars_poster = self.stars_poster[:-2]

    def db_import(self, row):
        """Imports row to Movie"""
        self.id = row[0]
        self.title = row[1]
        self.year = row[2]
        self.overview = row[3]
        self.genres = row[4]
        self.runtime = row[5]
        self.popularity = row[6]
        self.vote = row[7]
        self.vote_imdb = row[8]
        self.imdb_id = row[9]
        self.stars = row[10]
        self.stars_poster = row[11]
        self.character = row[12]
        self.poster = row[13]
        self.backdrop_path = row[14]
        self.trailer = row[15]
        self.file_name = row[16]
        self.folder = row[17]
        self.path = row[18]
        self.path = row[19]

    def __init__(self, flag, args):
        """imports data from DB if they exist else search for movies in specified directory"""
        if flag == True:
            self.db_make(args)
        else:
            self.db_import(args)

    def download_files(self):
        """Download files locally"""
        self.download_image(self.id, 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/' + self.poster, 'poster')
        self.download_image(self.id, 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/' + self.backdrop_path,
                            'backdrop')
        i = 0
        sp = self.stars_poster.split(', ')
        for stars_p in sp:
            if i <= 10:
                i += 1
                if stars_p == 'null':
                    from shutil import copyfile

                    path = '%s\\Papflix\\' + str(self.id) + '\\stars_posters\\'
                    dir_path = path % os.environ['APPDATA']
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    shutil.copy('../resources/unknown.png', dir_path + str(i) + '.png')
                else:
                    self.download_image(str(self.id) + '//stars_posters',
                                        'https://image.tmdb.org/t/p/w600_and_h900_bestv2/' + stars_p, i)

    def download_image(self, id, url, name):
        """Download images locally"""
        import os
        import requests
        path = '%s\\Papflix\\' + str(id)
        dir_path = path % os.environ['APPDATA']
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        complete_name = os.path.join(dir_path, str(name) + '.png')

        if not os.path.exists(complete_name):
            R = requests.get(url, allow_redirects=True)
            if R.status_code != 200:
                raise ConnectionError('could not download {}\nerror code: {}'.format(url, R.status_code))
            open(complete_name, 'wb').write(R.content)

    def db_make(self, args):
        """Imports args in DB"""
        self.file_name = args[0]
        self.folder = args[1]
        self.path = args[2]
        self.stars = ''
        self.stars_poster = ''
        self.character = ''
        extraction = self.extract_name_year(self.file_name)
        name = extraction[0]
        year = extraction[1]

        self.id = self.search_movie_json(name, year, self.folder, 1)
        self.json = self.get_json_movie(self.id)

        self.title = self.json['title']
        self.year = int(self.json['release_date'].split('-', 1)[0])
        self.overview = self.json['overview']
        self.vote = float(self.json['vote_average'])
        self.popularity = self.json['popularity']
        self.trailer = self.get_trailer(self.id)
        self.credits = self.get_credits(self.id)

        if len(self.json['genres']) != 0:
            for gen in self.json['genres']:
                self.genres += gen['name'] + ', '
            self.genres = self.genres[:-2]
        else:
            self.genres = ''
        if self.json['backdrop_path'] is None:
            self.backdrop_path = 'null'
        else:
            self.backdrop_path = self.json['backdrop_path']

        if self.json['poster_path'] is None:
            self.poster = 'null'
        else:
            self.poster = self.json['poster_path']

        if self.json['runtime'] is None:
            self.runtime = 'null'

        else:
            self.runtime = str(self.json['runtime'])
        if self.json['imdb_id'] is None:
            self.imdb_id = 'null'
        else:
            self.imdb_id = self.json['imdb_id']

