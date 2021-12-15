import sys
import pandas as pd


if __name__ == "__main__":
    frames = []
    for f in sys.argv[1:-1]:
        df = pd.read_csv(f, index_col=0)
        frames.append(df)
    frame = pd.concat(frames)
    if '1f1' in sys.argv:
        frame = frame.set_axis(['maxT = 1', 'maxT = 2', 'maxT = 4', 'maxT = 6', 'maxT = 8', 'maxT = 10'], axis=0)
    elif 'uniformf1' in sys.argv:
        frame = frame.set_axis(['mutUniform', 'mutShrink', 'mutNodeReplacement', 'mutInsert', 'crossLeafBiased'], axis=0)
    elif 'random_fullf1' in sys.argv:
        frame = frame.set_axis(['Random Walk', 'Grow', 'Full', 'Ramped'], axis=0)
    elif '8192f1' in sys.argv:
        frame = frame.set_axis(['8192', '4096', '2048', '1024', '512', '256', '128', '64', '32'], axis=0)
    else:
        frame = frame.set_axis(['Random Walk', 'Without Paths', 'Without Types', 'Without Random Walk'], axis=0)

    frame = frame.T
    with open(sys.argv[-1], 'w') as f:
       f.write(frame.to_markdown())

