import os
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class AgribusinessSystem(ABC):
    @abstractmethod
    def load_clean_data(self):
        pass

    @abstractmethod
    def run_analytics(self):
        pass

class FarmDataAnalyzer(AgribusinessSystem):
    def __init__(self, folder_path):
        self.__folder_path = folder_path  
        self.all_files = []
        self.combined_data = pd.DataFrame()

    def get_folder_path(self):
        return self.__folder_path

    def load_clean_data(self):
        if os.path.exists(self.get_folder_path()):
            folder_contents = os.listdir(self.get_folder_path())
            self.all_files = [f for f in folder_contents if f.endswith('.csv')]
            data_list = []
            for file in self.all_files:
                file_full_path = os.path.join(self.get_folder_path(), file)
                df = pd.read_csv(file_full_path)
                df.columns = df.columns.str.strip().str.lower()
                df['farm_name'] = file.replace('.csv', '')
                data_list.append(df)
            if data_list:
                self.combined_data = pd.concat(data_list, ignore_index=True)

class AdvancedFarmAnalyzer(FarmDataAnalyzer):
    def run_analytics(self):
        if self.combined_data.empty:
            print("No data found!")
            return
            
        temp_col = 'temperature'
        moist_col = 'soil_moisture' if 'soil_moisture' in self.combined_data.columns else 'soil moisture'
        
        if temp_col not in self.combined_data.columns:
            print(f"Column '{temp_col}' not found. Available columns: {list(self.combined_data.columns)}")
            return

        report = self.combined_data.groupby('farm_name')[[temp_col, moist_col]].mean()
        print("\n=== AGRIBUSINESS DATA REPORT ===")
        print(report)
        print("===============================\n")
        
        report[temp_col].plot(kind='bar', color='green', figsize=(10, 5))
        plt.title('Average Temperature Across Farms (AGE219 Project)')
        plt.xlabel('Farm Name')
        plt.ylabel('Average Temperature (Celsius)')
        plt.grid(axis='y', linestyle='--')
        plt.savefig('average_temperature_plot.png')
        print("Graph has been saved successfully as 'average_temperature_plot.png'!")
        plt.show()

if __name__ == "__main__":
    target_folder = "." 
    analyzer = AdvancedFarmAnalyzer(target_folder)
    analyzer.load_clean_data()
    analyzer.run_analytics()