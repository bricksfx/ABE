#coding=utf8
from .tree import tree


def generator_tree_for_user(user):
    alb1 = tree(4, [], [
        tree(1, [int(user.dataofuser.sex)], []),
        tree(1, [int(user.dataofuser.identity)], []),
        tree(1, [int(user.dataofuser.academy_id)+10], []),
        tree(1, [int(user.dataofuser.major_id)+50], []),
    ])
    print "user tree info", user.dataofuser.sex, user.dataofuser.identity, int(user.dataofuser.academy_id)+10, int(user.dataofuser.major_id)+50
    return alb1


def share_to_attr(share):
    share = str(share)
    attr = []
    tmp = share.split(":")
    print tmp
    if tmp[0] == '0':
        attr.append(1)
        attr.append(2)
    else:
        attr.append(int(tmp[0]))
    for i in range(1, 4):
        if tmp[i].find(',') != -1:
            for item in tmp[i].split(','):
                if i == 2:
                    attr.append(int(item) + 10)
                elif i == 3:
                    attr.append(int(item) + 50)
                else:
                    attr.append(int(item))
        else:
            if i == 2:
                    attr.append(int(tmp[i]) + 10)
            elif i == 3:
                attr.append(int(tmp[i]) + 50)
            else:
                attr.append(int(tmp[i]))
    return attr

def key_encrypt(attr):
    pass

def test():
    share_to_attr("0:4,6:9,10,11:16,19,23")

if __name__ == '__main__':
    test()