import json
import matplotlib.pyplot as plt
import numpy as np
import os


class Plot:

    def check_user_entries(self):
        with open('data_files/records.json', 'r') as f:
            data = json.load(f)
        if data:
            return True
        return False

    def create_and_save_chart(self):

        with open('data_files/records.json', 'r') as f:
            data = json.load(f)


        revenue = {dish: info['price'] * info['quantity'] for dish, info in data.items()}
        dishes = list(revenue.keys())
        revenues = list(revenue.values())

        max_revenue = max(revenues)
        y_max_limit = max_revenue + 100

        fig, ax = plt.subplots(figsize=(8, 5))
        bar_width = 0.4
        bar_positions = np.arange(len(dishes))
        bar_positions = bar_positions * 0.8

        bars = ax.bar(bar_positions, revenues, width=bar_width, color=plt.cm.Paired(np.arange(len(dishes))))

        ax.set_xlabel('Dish', fontsize=12, fontweight='bold')
        ax.set_ylabel('Revenue', fontsize=12, fontweight='bold')
        ax.set_title('Revenue Distribution by Dish', fontsize=14, fontweight='bold')
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(dishes, rotation=45, ha='right', fontsize=10)
        ax.set_yticks(np.arange(0, y_max_limit + 100, 100))
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.set_ylim(0, y_max_limit)


        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, f'{yval}', ha='center', va='bottom', fontsize=10,
                    fontweight='bold')

        desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop_directory):
            os.makedirs(desktop_directory)

        output_file = os.path.join(desktop_directory, "revenue_distribution.png")
        try:
            plt.tight_layout(rect=[0, 0.05, 1, 1])
            plt.savefig(output_file, format='png')
            plt.close(fig)
            return 1, output_file
        except Exception as e:
            return 0, 'Error occurred.'

