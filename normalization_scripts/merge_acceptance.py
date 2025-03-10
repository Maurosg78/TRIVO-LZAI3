import pandas as pd

def merge_acceptance():
    df_main = pd.read_csv("final_dataset.csv", dtype=str)
    df_scores = pd.read_csv("acceptance_scores.csv", dtype=str)

    df_merged = pd.merge(df_main, df_scores, on="FoodID", how="left")
    df_merged.to_csv("final_dataset_with_score.csv", index=False)
    print("[OK] final_dataset_with_score.csv generado")

if __name__ == "__main__":
    merge_acceptance()
