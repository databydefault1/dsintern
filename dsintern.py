import pandas as pd
import streamlit as st

df = pd.read_csv("sample-data/product_usage_events.csv")

rows_before = len(df)

df["team"] = df["team"].str.title()
df = df[df["notes"] != "duplicate export row"]
df = df[~df["notes"].str.contains("demo account")]
df["median_confidence"] = pd.to_numeric(df["median_confidence"], errors="coerce")

st.title("SignalDesk workflow check")
st.write("Rows before cleaning:", rows_before)
st.write("Rows after cleaning:", len(df))

scorecard = df.groupby("workflow").agg(
    sessions=("sessions", "sum"),
    accepted=("accepted_output", "sum"),
    flagged=("flagged_for_review", "sum"),
)

scorecard["Accept rate"] = (scorecard["accepted"] / scorecard["sessions"] * 100).round(1).astype(str) + "%"
scorecard["Flag rate"] = (scorecard["flagged"] / scorecard["sessions"] * 100).round(1).astype(str) + "%"

st.header("Scorecard")
st.dataframe(scorecard)


st.write("Lead summary and Reply draft are basically tied at 61%. Feedback clustering is 16 points behind at 44%, so Product is throwing away more than half of what it makes. Reply draft also gets flagged about twice as often as Lead summary even though their accept rates match.")

st.header("Which metrics to trust")

st.write("Accept rate: I trust this one but only because someone chose to keep the output, not that the output was right.")
st.write("Flag rate: This was hard to read because it went up when output got worse and also when review were stricter, and this data can't separate the two.")
st.write("Median confidence: I don't trust it because on Aug 7 the Support queue rows show confidence going up from 0.88 to 0.91 while accept rate dropped from 64% to 27% and rating dropped from 4.1 to 2.1.")

st.header("What to look at next")

st.write("1. Support's queue numbers all dropped on Aug 7, and the note on that row says the review policy changed mid-day, so I'd check what that change was before blaming the model.")
st.write("2. Every row on Aug 4 says new prompt version, so all three workflows switched at once and nothing stayed on the old one to compare them against each other so i would roll the next one out to one team first.")
st.write("3. Aug 7 only has 4 rows when every other day has 6 because Sales manual and Support manual never showed up, so the day looks smaller than it was and i would check whether those runs happened before comparing it to the other days.")

st.dataframe(df)
