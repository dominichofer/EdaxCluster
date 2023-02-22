from cluster import TaskDispatchClient
from core import parse_game_score_file, write_game_score_file, undefined_score, solve_game_score_file
import edax

def on_report(index: int, result):
    print(index, result)


if __name__ == '__main__':
    #pos = [0] * 64
    #solved = [0] * 64
    files = [
        r'G:\Edax4.4_level_0_vs_Edax4.4_level_0_from_e54.gs',
        r'G:\Edax4.4_level_5_vs_Edax4.4_level_5_from_e54.gs',
        r'G:\Edax4.4_level_10_vs_Edax4.4_level_10_from_e54.gs',
        r'G:\Edax4.4_level_15_vs_Edax4.4_level_15_from_e54.gs',
        r'G:\Edax4.4_level_20_vs_Edax4.4_level_20_from_e54.gs',
    ]

    #ip = sys.argv[1]
    #ip = 'ec2-44-195-46-122.compute-1.amazonaws.com'
    client = TaskDispatchClient('localhost')

    engine = edax.Engine(r'G:\edax-ms-windows\edax-4.4', 60)
    
    tasks = []
    for file_index, f in enumerate(files):
        game_scores = parse_game_score_file(f)
    #    for game_index, gs in enumerate(game_scores):
    #        for pos_index, pos in enumerate(gs.positions()):
    #            if pos.empty_count() <= 29 and gs.scores[pos_index] == undefined_score:
    #                line = engine.solve(pos)[0]
    #                print(line)
    #                gs.scores[pos_index] = line.score
    #    write_game_score_file(game_scores, f)
        tasks += [
            (pos, file_index, game_index, pos_index)
            for game_index, gs in enumerate(game_scores)
            for pos_index, pos in enumerate(gs.positions())
            if pos.empty_count() <= 30 and gs.scores[pos_index] == undefined_score
            ]
        
    results = client.dispatch([(str(t[0]), 60) for t in tasks], on_report)
    
    #for file_index, f in enumerate(files):
    #    game_scores = parse_game_score_file(f)

    #    for t, r in zip(tasks, results):
    #        if t[1] == file_index:
    #            game_scores[t[2]].scores[t[3]] = r[1]

    #    write_game_score_file(game_scores, f)

        #game_scores = parse_game_score_file(f)
        #for gs in game_scores:
        #    for p, s in gs.pos_scores():
        #        pos[p.empty_count()] += 1
        #        if s == undefined_score and p.empty_count() <= 28:
        #            print(p)
                #if p.empty_count() == 10:
                #    pos.append((str(p), 10))
    #print(pos)
    #print(solved)
    
    #results = client.dispatch(task, on_report)
    #print(results)
