from argparse import ArgumentParser

from colbert.evaluation.loaders import load_queries, load_qrels,load_topK_pids

from colbert.evaluation.metrics import Metrics


def main():
    parser = ArgumentParser(description="")
    parser.add_argument('--qrels', dest='qrels', default=None)
    parser.add_argument('--queries', dest='queries', default=None)
    parser.add_argument('--topk', dest='topK', required=True)
    args = parser.parse_args()

    args.qrels = load_qrels(args.qrels)
    args.queries = load_queries(args.queries)
    args.topK_pids, args.qrels = load_topK_pids(args.topK, args.qrels)
    qrels, queries, topK_pids = args.qrels, args.queries, args.topK_pids

    metrics = Metrics(mrr_depths={10, 100}, recall_depths={50, 200, 1000},
                      success_depths={5, 10, 20, 50, 100, 1000},
                      total_queries=len(queries))

    keys = sorted(list(queries.keys()))
    for query_idx, qid in enumerate(keys):
        ranking = [(None, pid, None) for pid in topK_pids[qid]]
        metrics.add(query_idx, qid, ranking, qrels[qid])

        for i, (score, pid, passage) in enumerate(ranking):
            if pid in qrels[qid]:
                print("\n#> Found", pid, "at position", i + 1, "with score", score)
                print(passage)
                break

        metrics.print_metrics(query_idx)


if __name__ == "__main__":
    main()