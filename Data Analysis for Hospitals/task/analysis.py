import pandas as pd


class DataAnalyzer:
    def __init__(self, *paths):
        self.paths = paths
        self.datasets = []
        self.read_data()
        self.df = pd.concat(self.datasets, ignore_index=True)
        self.stats = {}

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

    def statistics(self):
        self.stats['hospital'] = self.df.hospital.mode()[0]
        self.stats['stomach'] = (self.df.loc[(self.df.hospital == 'general') &
                                             (self.df.diagnosis == 'stomach')].shape[0] /
                                 self.df.loc[self.df.hospital == 'general'].shape[0])
        self.stats['dislocation'] = (self.df.loc[(self.df.hospital == 'sports') &
                                                 (self.df.diagnosis == 'dislocation')].shape[0] /
                                     self.df.loc[self.df.hospital == 'sports'].shape[0])
        ages = self.df.groupby('hospital').agg({'age': 'median'})
        self.stats['age_diff'] = ages.loc['general'] - ages.loc['sports']
        print(self.df.pivot_table(index='hospital', columns='blood_test', values='age', aggfunc='count'))


def main():
    pd.set_option('display.max_column', 8)

    analyzer = DataAnalyzer('test/data/general.csv', 'test/data/prenatal.csv', 'test/data/sports.csv')
    analyzer.preprocess()
    analyzer.statistics()

    print(f"The answer to the 1st question is {analyzer.stats['hospital']}\n"
          f"The answer to the 2st question is {analyzer.stats['stomach']:.3f}\n"
          f"The answer to the 3st question is {analyzer.stats['dislocation']:.3f}\n"
          f"The answer to the 4st question is {analyzer.stats['age_diff']}\n"
          f"The answer to the 5st question is {analyzer.stats['hospital']}, "
          f"{analyzer.stats['hospital']} blood tests")
    print(analyzer.df.blood_test.value_counts())


if __name__ == '__main__':
    main()
