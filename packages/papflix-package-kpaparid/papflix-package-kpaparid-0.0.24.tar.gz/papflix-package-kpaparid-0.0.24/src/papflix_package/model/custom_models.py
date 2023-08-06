
from PySide2.QtCore import *
from PySide2.QtGui import *

class PersonModel(QAbstractListModel):
    TitleRole = Qt.UserRole + 1
    YearRole = Qt.UserRole + 2
    OverviewRole = Qt.UserRole + 3
    PosterRole = Qt.UserRole + 4
    VoteRole = Qt.UserRole + 5
    RuntimeRole = Qt.UserRole + 6
    GenreRole = Qt.UserRole + 7
    StarsRole = Qt.UserRole + 8
    StarsPosterRole = Qt.UserRole + 9
    CharactersRole = Qt.UserRole + 10
    TrailerRole = Qt.UserRole + 11
    BackdropPathRole = Qt.UserRole + 12
    PathRole = Qt.UserRole + 13

    personChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.persons = []

    def clearAll(self):
        self.beginResetModel()
        self.persons.clear()
        self.endResetModel()
        print('clearing Model')
    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if role == PersonModel.TitleRole:
            return self.persons[row]["title1"]
        if role == PersonModel.YearRole:
            return self.persons[row]["year1"]
        if role == PersonModel.OverviewRole:
            return self.persons[row]["overview1"]
        if role == PersonModel.PosterRole:
            return self.persons[row]["poster1"]
        if role == PersonModel.VoteRole:
            return self.persons[row]["vote1"]
        if role == PersonModel.RuntimeRole:
            return self.persons[row]["runtime1"]
        if role == PersonModel.GenreRole:
            return self.persons[row]["genre1"]
        if role == PersonModel.StarsRole:
            return self.persons[row]["stars1"]
        if role == PersonModel.StarsPosterRole:
            return self.persons[row]["starsPoster1"]
        if role == PersonModel.CharactersRole:
            return self.persons[row]["characters1"]
        if role == PersonModel.TrailerRole:
            return self.persons[row]["trailer1"]   
        if role == PersonModel.BackdropPathRole:
            return self.persons[row]["backdrop_path1"]  
        if role == PersonModel.PathRole:
            return self.persons[row]["path1"]               
    def rowCount(self, parent=QModelIndex()):
        return len(self.persons)

    def roleNames(self):
        return {
            PersonModel.TitleRole: b'title1',
            PersonModel.YearRole: b'year1',
            PersonModel.OverviewRole: b'overview1',
            PersonModel.PosterRole: b'poster1',
            PersonModel.VoteRole: b'vote1',
            PersonModel.RuntimeRole: b'runtime1',
            PersonModel.GenreRole: b'genre1',
            PersonModel.StarsRole: b'stars1',
            PersonModel.StarsPosterRole: b'starsPoster1',
            PersonModel.CharactersRole: b'characters1',
            PersonModel.TrailerRole: b'trailer1',
            PersonModel.BackdropPathRole: b'backdrop_path1',
            PersonModel.PathRole: b'path1'
        }

    @Slot(str, str)
    def addPerson(self, title, year, overview, poster, vote, runtime, genre, stars, starsPoster, characters, trailer, backdrop_path, path):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        

        s_p = starsPoster.split(', ')
        starsPoster = ''
        for p in s_p:
            if(p == 'null'):
                p = '../resources/unknown.png'
            else:
                p = 'https://image.tmdb.org/t/p/w138_and_h175_face/'+p   
            starsPoster += ', ' + p

        if(poster == 'null'): poster = '../resources/unknown.png'
        
        
        starsPoster = starsPoster[2:]       
        self.persons.append({"title1":title, "poster1":'https://image.tmdb.org/t/p/w600_and_h900_bestv2/'+poster, "overview1":overview,
                             "year1":year, "vote1":vote, "runtime1":runtime,
                             "genre1":genre, "stars1":stars, 'starsPoster1':starsPoster,
                             "characters1":characters, "trailer1":trailer, "backdrop_path1":'https://image.tmdb.org/t/p/w1920_and_h800_multi_faces/'+backdrop_path, "path1":path})
        self.endInsertRows()


    @Slot(int)
    def deletePerson(self, row):
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self.persons[row]
        self.endRemoveRows()
