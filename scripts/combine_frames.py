import sys
import pandas as pd


if __name__ == "__main__":
    frames = []
    for f in sys.argv[1:-1]:
        df = pd.read_csv(f, index_col=0)
        frames.append(df)
    frame = pd.concat(frames, axis=1)
    if 'celoe' in frame.columns:
        frame = frame.set_axis(['EvoLearner', 'SPaCEL', 'CELOE',
                                'OCEL', 'Aleph'], axis=1)
        titles = ["EvoLearner", "CELOE", "OCEL", "Aleph", "SPaCEL"]
        frame = frame.reindex(columns=titles)
    elif '1f1' in sys.argv:
        frame = frame.set_axis(['maxT = 1', 'maxT = 2', 'maxT = 4',
                                'maxT = 6'],
                               axis=1)
    elif 'uniformf1' in sys.argv:
        frame = frame.set_axis(['mutUniform', 'mutShrink',
                                'mutNodeReplacement', 'mutInsert'], axis=1)
    elif 'random_fullf1' in sys.argv:
        frame = frame.set_axis(['Random Walk', 'Grow', 'Full', 'Ramped'],
                               axis=1)
    elif '8192f1' in sys.argv:
        frame = frame.set_axis(['8192', '4096', '2048', '1024',
                                '512', '256', '128', '64', '32'], axis=1)
    elif 'random_walkf1' in sys.argv:
        frame = frame.set_axis(['Random Walk', 'Without Paths',
                                'Without Types', 'Without Random Walk'],
                               axis=1)
    else:
        frame = frame.set_axis(['EvoLearner', 'WithoutRandomWalkInit',
                                'WithoutDataProperties', 'WithoutBoth'],
                               axis=1)

    with open(sys.argv[-1], 'w') as f:
        f.write(frame.to_markdown())
