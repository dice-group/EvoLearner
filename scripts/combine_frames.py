import sys
import pandas as pd


if __name__ == "__main__":
    frames = []
    for f in sys.argv[1:-1]:
        df = pd.read_csv(f, index_col=0)
        frames.append(df)
    frame = pd.concat(frames)
    if 'celoe' in frame.index.values:
        frame = frame.set_axis(['EvoLearner', 'SPaCEL', 'CELOE', 'OCEL', 'Aleph'], axis=0)
    else:
        frame = frame.set_axis(['EvoLearner', 'WithoutRandomWalkInit', 'WithoutDataProperties', 'WithoutBoth'], axis=0)

    frame = frame.T
    if 'CELOE' in frame.columns:
        titles = ["EvoLearner", "CELOE", "OCEL", "Aleph", "SPaCEL"]
        frame = frame.reindex(columns=titles)
    with open(sys.argv[-1], 'w') as f:
       f.write(frame.to_markdown())

