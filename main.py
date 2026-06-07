import os
import pandas as pd
import matplotlib.pyplot as plt

class FarmDataAnalyzer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.combined_data = pd.DataFrame()

    def load_clean_data(self):
        all_data = []
        for file in os.listdir(self.folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(self.folder_path, file)
                df = pd.read_csv(file_path)
                farm_name = os.path.splitext(file)[0]
                df['Farm_Name'] = farm_name
                all_data.append(df)
        if all_data:
            self.combined_data = pd.concat(all_data, ignore_index=True)
            print("Data loaded successfully!")
        else:
            print("No CSV files found.")

class AdvancedFarmAnalyzer(FarmDataAnalyzer):
    def run_analytics(self):
        if self.combined_data.empty:
            print("No data available to analyze.")
            return
        
        # Checking correct column name dynamically
        temp_col = None
        for col in self.combined_data.columns:
            if 'temp' in col.lower():
                temp_col = col
                break
                
        if not temp_col:
            print("Temperature column not found.")
            return

        report = self.combined_data.groupby('Farm_Name')[temp_col].mean().reset_index()
        print("\n--- Average Temperature Across Farms ---")
        print(report)
        
        # Plotting the analytics graph
        plt.figure(figsize=(10, 5))
        plt.bar(report['Farm_Name'], report[temp_col], color='green', width=0.5)
        plt.title('Average Temperature Across Farms (AGE219 Project)')
        plt.xlabel('Farm Name')
        plt.ylabel('Average Temperature (Celsius)')
        plt.grid(axis='y', linestyle='--')
        plt.savefig('average_temperature_plot.png')
        print("Graph has been saved successfully as 'average_temperature_plot.png'")
        plt.show()

if __name__ == "__main__":
    target_folder = "."
    analyzer = AdvancedFarmAnalyzer(target_folder)
    analyzer.load_clean_data()
    analyzer.run_analytics()