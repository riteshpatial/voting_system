import pandas as pd

df = pd.read_csv("backend/logs/voting_logs.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Count votes per voter
vote_counts = df.groupby("voter").size().reset_index(name="votes")

# Time difference between votes
df = df.sort_values(["voter", "timestamp"])
df["time_diff"] = df.groupby("voter")["timestamp"].diff().dt.seconds

anomalies = []

for _, row in vote_counts.iterrows():
    if row["votes"] > 1:
        anomalies.append({
            "voter": row["voter"],
            "reason": "Multiple votes",
            "votes": row["votes"]
        })

fast_votes = df[df["time_diff"] < 10]

for voter in fast_votes["voter"].unique():
    anomalies.append({
        "voter": voter,
        "reason": "Votes too fast",
        "votes": int(vote_counts[vote_counts["voter"] == voter]["votes"])
    })

print("\n🚨 ANOMALY REPORT")
for a in anomalies:
    print(a)
