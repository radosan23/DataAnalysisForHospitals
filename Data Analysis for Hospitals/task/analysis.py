import pandas as pd
import matplotlib.pyplot as plt


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
        self.stats['age_diff'] = abs(ages.loc['general'].values[0] - ages.loc['sports'].values[0])
        blood_t = self.df.pivot_table(index='hospital', columns='blood_test', values='age', aggfunc='count')
        self.stats['bloodiest'] = blood_t.t.idxmax()
        self.stats['n_blood_t'] = blood_t.t.agg('max').astype('int')

    def visualize(self):
        bins = [0, 15, 35, 55, 70, 80]
        self.df.plot(y=['age'], kind='hist', bins=bins)
        plt.show()
        self.df['diagnosis'].value_counts().plot(kind='pie')
        plt.show()
        plt.violinplot([self.df['height'], self.df.loc[self.df.hospital == 'general', 'height'],
                        self.df.loc[self.df.hospital == 'prenatal', 'height'],
                        self.df.loc[self.df.hospital == 'sports', 'height']])
        plt.title('patients age')
        plt.show()


def main():
    pd.set_option('display.max_column', 8)

    analyzer = DataAnalyzer('test/data/general.csv', 'test/data/prenatal.csv', 'test/data/sports.csv')
    analyzer.preprocess()
    analyzer.visualize()

    print(f"The answer to the 1st question: 15-35\n"
          f"The answer to the 2nd question: pregnancy\n"
          f"The answer to the 3rd question: because sports hospital measure height in feet, others in meters")


if __name__ == '__main__':
    main()
