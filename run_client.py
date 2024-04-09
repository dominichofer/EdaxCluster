import logging
import sys
from reversi import ScoredGame, read_file, write_file, scored_positions, empty_count_range_filtered, positions
from rte import RemoteServer
from edax_cluster import EdaxBatchClient, EdaxTask

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"

    FILE = r"C:\Users\Dominic\source\repos\python-reversi\data\random_selfplay_from_e54.gs"
    scored_games: list[ScoredGame] = read_file(FILE)
    scored_pos = empty_count_range_filtered(scored_positions(scored_games), 0, 30)
    unsolved_pos = [sp.pos for sp in scored_pos if not sp.is_score_defined()]
    print(len(unsolved_pos))

    server = RemoteServer(f"{ip}:50051")
    client = EdaxBatchClient(server, refresh_time=10)
    tasks = [EdaxTask(pos, level=60) for pos in unsolved_pos]
    results = client.solve(tasks)

    scores = [r.score for r in results if r is not None]
    pos_score = dict(zip(unsolved_pos, scores))

    # Update the scores
    for sg in scored_games:
        for i, pos in enumerate(positions(sg)):
            if pos in pos_score:
                sg.scores[i] = pos_score[pos]

    write_file(FILE, scored_games)
