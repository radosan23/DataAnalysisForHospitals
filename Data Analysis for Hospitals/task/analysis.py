import pandas as pd


class DataAnalyzer:
    def __init__(self, *paths):
        self.paths = paths
        self.datasets = []
        self.read_data()
        self.df = pd.concat(self.datasets, ignore_index=True)

    def read_data(self):
        for path in self.paths:
            self.datasets.append(pd.read_csv(path, index_col=0))
        for dataset in self.datasets[1:]:
            dataset.columns = self.datasets[0].columns

    def preprocess(self):
        self.df.dropna(axis=0, how='all', inplace=True)
        self.df['gender'].replace({'male': 'm', 'man': 'm', 'female': 'f', 'woman': 'f'}, inplace=True)
        self.df.loc[self.df.hospital == 'prenatal', 'gender'] = (
            self.df.loc[self.df.hospital == 'prenatal', 'gender'].fillna('f'))
        cols = ['blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
        self.df[cols] = self.df[cols].fillna(0)


def main():
    pd.set_option('display.max_column', 8)

    analyzer = DataAnalyzer('test/data/general.csv', 'test/data/prenatal.csv', 'test/data/sports.csv')
    analyzer.preprocess()

    print('Data shape:', analyzer.df.shape)
    print(analyzer.df.sample(n=20, random_state=30))


if __name__ == '__main__':
    main()
