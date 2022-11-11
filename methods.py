import BeFake.BeFake as BeFake

#DATA_DIR = "BeFake/data"
#TOKEN_PATH = "BeFake/token.txt"

# not yet implemented...
def get_comments(post_id, content):
    bf = BeFake.BeFake()
    bf.load()
    return bf.get_comments(post_id, content)


def add_comment(post_id, content):
    bf = BeFake.BeFake()
    bf.load()
    return bf.add_comment(post_id, content)


if __name__ == "__main__":
    pass