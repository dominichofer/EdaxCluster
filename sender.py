import socket
import sys
from workspread import Client
from core import parse_game_score_file, Position


if __name__ == '__main__':
    #ip = sys.argv[1]
    #port = int(sys.argv[2])
    ip = 'ec2-54-144-141-110.compute-1.amazonaws.com'
    port = 12350

    pos = []
    files = [
        r'G:\Reversi2\Edax4.4_level_0_vs_Edax4.4_level_0_from_e54.gs',
        #r'G:\Reversi2\Edax4.4_level_5_vs_Edax4.4_level_5_from_e54.gs',
        #r'G:\Reversi2\Edax4.4_level_10_vs_Edax4.4_level_10_from_e54.gs',
        #r'G:\Reversi2\Edax4.4_level_15_vs_Edax4.4_level_15_from_e54.gs',
        #r'G:\Reversi2\Edax4.4_level_20_vs_Edax4.4_level_20_from_e54.gs',
    ]
    for f in files:
        game_scores = parse_game_score_file(f)
        for gs in game_scores:
            for p in gs.positions():
                if p.empty_count() == 10:
                    pos.append(str(p) + '10')
    print(pos)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    client = Client(sock, 1024 * 1024)

    result = client.run(pos)
    print(result)
