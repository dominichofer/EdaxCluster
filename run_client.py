import logging
from reversi import *
from rte import RemoteServer
from edax_cluster import EdaxBatchClient, EdaxTask

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    file = r"C:\Users\Dominic\source\repos\python-reversi\data\random_selfplay_from_e54.gs"
    scored_games: list[ScoredGame] = read_file(file)
    scored_pos = empty_count_range_filtered(scored_positions(scored_games), 29, 30)
    unsolved_pos = [sp.pos for sp in scored_pos if not sp.is_score_defined()]
    print(len(unsolved_pos))

    server = RemoteServer("localhost:50051")
    client = EdaxBatchClient(server, refresh_time=1)
    tasks = [EdaxTask(pos, 60) for pos in unsolved_pos]
    results = client.solve(tasks)

    scores = [r.score for r in results if r is not None]
    pos_score = {pos: score for pos, score in zip(unsolved_pos, scores)}

    # Update the scores
    for sg in scored_games:
        for i, pos in enumerate(positions(sg)):
            if pos in pos_score:
                sg.scores[i] = pos_score[pos]

    print(scored_games)

    write_file(file, scored_games)
