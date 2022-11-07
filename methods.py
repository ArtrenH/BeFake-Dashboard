
import BeFake.BeFake as BeFake

#DATA_DIR = "BeFake/data"
#TOKEN_PATH = "BeFake/token.txt"


def add_comment(post_id, content):
    bf = BeFake.BeFake()
    bf.load()
    return bf.add_comment(post_id, content)


if __name__ == "__main__":
    c = add_comment("8E1prcVz_cxgs5XoMdp1Z", "Noch ein kurzer Test")
    print(c)
