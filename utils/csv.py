# Paths
CSV_PATH = "data/csv"
MOVIES_CSV = CSV_PATH + '/movies.csv'
NEXT_MOVIE_CSV = CSV_PATH + '/next_movie.csv'


def get_next_movie():
    with open(NEXT_MOVIE_CSV, 'r') as f:
        line = f.read().splitlines()[0].split('|')
        # title, year, chooser
        return line[0], line[1], line[2]


def get_movie(idx):
    with open(MOVIES_CSV, 'r') as f:
        lines = f.read().splitlines()
        line = lines[idx].split('|')
    title = line[0]
    year = line[1]
    return title, year


def get_entry(title, member):
    with open(CSV_PATH + "/{}.csv".format(member.lower()), 'r') as f:
        lines = f.read().splitlines()
        for l in lines:
            if l.split('|')[0] == title:
                return l
    return None


def append_movie(title, year, date, chooser):
    with open(MOVIES_CSV, 'a') as f:
        f.write("{}|{}|{}|{}\n".format(title, year, date, chooser))


def update_next_movie(title, year, chooser):
    with open(NEXT_MOVIE_CSV, 'w') as f:
        f.write("{}|{}|{}\n".format(title, year, chooser))