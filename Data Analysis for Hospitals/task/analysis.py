import pandas as pd


def main():
    pd.set_option('display.max_column', 8)

    general = pd.read_csv('test/data/general.csv')
    prenatal = pd.read_csv('test/data/prenatal.csv')
    sports = pd.read_csv('test/data/sports.csv')

    for df in [general, prenatal, sports]:
        print(df.head(20))


if __name__ == '__main__':
    main()
