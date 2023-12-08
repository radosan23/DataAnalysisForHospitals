import pandas as pd


def main():
    pd.set_option('display.max_column', 8)

    general = pd.read_csv('test/data/general.csv', index_col=0)
    prenatal = pd.read_csv('test/data/prenatal.csv', index_col=0)
    sports = pd.read_csv('test/data/sports.csv', index_col=0)

    prenatal.columns = sports.columns = general.columns
    df = pd.concat([general, prenatal, sports], ignore_index=True)
    print(df.sample(n=20, random_state=30))


if __name__ == '__main__':
    main()
