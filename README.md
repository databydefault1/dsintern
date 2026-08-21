\#SignalDesk workflow check



\*\*Track:\*\* A (fictional domain packet)



\## What this is

A SignalDesk report that takes usage export, cleans it, and

answers three things for the team: what's working, what looks off, and

what to look at next.



\## Who it's for



The product team that runs  SignalDesk that is meant to be rerun on the

next export.



\## Data



sample-data/product\_usage\_events.csv from the challenge repo. 41 rows,

Aug 1 to Aug 7 2026, three workflows across three teams.



\## Assumptions



The file is 41 rows, so I read it directly rather than writing

&#x20; detection code. On a larger export I'd run df.dublicated on the measurement columns.



\## Issues I found

* There were duplicate rows on Aug 5 that I dropped. One was an export

&#x20; bug that wrote the same row out twice. The other came from a demo

&#x20; account, so it isn't real user data.

* median\_confidence had an "n/a" in it, so I checked the column's data

&#x20; type and it came back as a string. I converted

&#x20; the column to numeric with errors="coerce"

* The team column had "product" lowercase on one row so I normalized it so that

&#x20; grouping doesn't split Product into two teams.



\## What I'd do next

* I would split the numbers by source instead of rolling manual and

&#x20; automated runs into one number. Without separating them I can't see

&#x20; the real difference in accept and flag rates, and that's probably

&#x20; where the Aug 7 drop in Support would actually show up.



\## How to run

pip install pandas streamlit



python -m streamlit run dsintern.py

