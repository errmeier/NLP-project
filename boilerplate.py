import sys

def desc_move(move_str):
    out_str = ''
    move = move_str.split()

    check = 'check' in move
    mate = 'checkmate' in move
    promote = 'promote' in move
    capture = 'capture' in move
    piece = move[2]

    if promote:
        if mate:
            out_str = 'The ' + str(move[3][0])+ '-pawn promotes to a ' +
            move[move.index('promote')+1] + ' and delivers checkmate'
        elif check:
            out_str = 'The ' + str(move[3][0]) + '-pawn promotes to a ' + piece + ' and checks the king'
        else:
            out_str = 'The ' + str(move[3][0]) + '-pawn promotes to a ' + piece
    elif capture:
        if mate:
            out_str = 'The ' + piece + ' captures on ' + move[4] + ' and delivers checkmate'
        if check:
            out_str = 'The ' + piece + ' captures on ' + move[4] + ' and checks the king'
        else:
            out_str = 'The ' + piece + ' captures on ' + move[4]
    else:
        if mate:
            out_str = 'The ' + piece + ' moves to ' + move[4] + ' and delivers checkmate'
        elif check:
            out_str = 'The ' + piece + ' moves to ' + move[4] + ' and checks the king'
        else:
            out_str = 'The ' + piece + ' moves to ' + move[4]

    return out_str

if __name__ == "__main__":
    for line in open(sys.argv[1]).readlines():
        print(desc_move(line.strip()))
