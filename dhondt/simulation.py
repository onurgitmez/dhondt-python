import pandas as pd
from typing import List, Dict, Union

def simulate_election(df: pd.DataFrame, 
                      district_col: str, 
                      seats_col: str, 
                      parties: List[str], 
                      threshold: float = 0.0) -> Dict[str, Union[Dict[str, int], pd.DataFrame]]:

    df[parties] = df[parties].fillna(0)
    total_votes = df[parties].sum()
    vote_share = total_votes / total_votes.sum()
    eligible_parties = vote_share[vote_share >= threshold].index.tolist()

    for party in parties:
        df[party + '_seats'] = 0

    for district in df[district_col].unique():
        district_data = df[df[district_col] == district]
        votes = district_data[eligible_parties].iloc[0]
        seats = district_data[seats_col].iloc[0]

        if pd.isna(seats) or seats <= 0:
            continue

        results = {party: 0 for party in eligible_parties}
        for _ in range(int(seats)):
            max_votes = 0
            winner = ''
            for party in eligible_parties:
                party_votes = votes[party]
                party_seats = results[party]
                quotient = party_votes / (party_seats + 1)
                if quotient > max_votes:
                    max_votes = quotient
                    winner = party
            results[winner] += 1

        for party, seat_count in results.items():
            df.loc[df[district_col] == district, party + '_seats'] = seat_count

    total_row = pd.Series(index=df.columns)
    total_row['label'] = "Total"
    total_row[seats_col] = df[seats_col].sum()

    for party in parties:
        total_row[party] = df[party].fillna(0).sum()
        total_row[party + '_seats'] = df[party + '_seats'].sum()

    totals_df = pd.DataFrame([total_row])
    total_seats = {party: total_row[party + '_seats'] for party in parties}

    # Print the total seats in a readable format
    for party, seats in total_seats.items():
        print(f"{party} seats: {seats}")

    return {"totals": total_seats, "df_with_seats": df, "totals_df": totals_df}
