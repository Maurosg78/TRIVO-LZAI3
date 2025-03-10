# merge_acceptance.py
import pandas as pd

def merge_acceptance():
    df_main = pd.read_csv("final_dataset_with_score_NORMALIZADO.csv", dtype=str)
    df_scores = pd.read_csv("normalization_scripts/acceptance_scores_NORMALIZADO.csv", dtype=str)

    df_merged = pd.merge(df_main, df_scores, on="FoodID", how="left")
    df_merged.to_csv("final_dataset_with_score_merged.csv", index=False)
    print("[OK] final_dataset_with_score_merged.csv generado")

if __name__ == "__main__":
    merge_acceptance()
