import logging
import sys
from reversi import ScoredGame, read_file, write_file, scored_positions, empty_count_range_filtered, positions
from rte import RemoteServer
from edax_cluster import EdaxBatchClient, EdaxTask

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    file = sys.argv[1]
    ip = sys.argv[2] if len(sys.argv) > 1 else "localhost"
    lower_empty_count = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    upper_empty_count = int(sys.argv[4]) if len(sys.argv) > 4 else 64

    scored_games: list[ScoredGame] = read_file(file)
    scored_pos = empty_count_range_filtered(scored_positions(scored_games), 0, 30)
    unsolved_pos = [sp.pos for sp in scored_pos if not sp.is_score_defined()]
    print(len(unsolved_pos))

    server = RemoteServer(f"{ip}:50051")
    client = EdaxBatchClient(server, refresh_time=0.01, attempts=100)
    tasks = [EdaxTask(pos, level=60) for pos in unsolved_pos]
    results = client.solve(tasks)

    pos_score = {pos: r.score for pos, r in zip(unsolved_pos, results) if r is not None}

    # Update the scores
    for sg in scored_games:
        for i, pos in enumerate(positions(sg)):
            if pos in pos_score:
                sg.scores[i] = pos_score[pos]

    write_file(file, scored_games)
