import pandas as pd
from typing import List, Dict, Union

def simulate_election(df: pd.DataFrame, 
                      district_col: str, 
                      seats_col: str, 
                      parties: List[str], 
                      threshold: float = 0.0) -> Dict[str, Union[Dict[str, int], pd.DataFrame]]:
    """
    Simulate an election using the D'Hondt method.
    
    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame with election data. Must include a column for each party's votes, 
        a district names column, and a seats per district column.
    district_col : str
        Column name for district names.
    seats_col : str
        Column name indicating the number of seats in each district.
    parties : List[str]
        List of columns representing votes for each party.
    threshold : float, optional
        Minimum vote share for a party to be eligible for seats. Defaults to 0.

    Returns:
    -------
    dict
        A dictionary with two keys:
        - totals: A dictionary with each party's total seats.
        - df_with_seats: A DataFrame showing seats distribution across districts.
    """

    # Calculate vote shares
    total_votes = df[parties].sum()
    vote_share = total_votes / total_votes.sum()

    # Filter eligible parties based on the threshold
    eligible_parties = vote_share[vote_share >= threshold].index.tolist()

    if not eligible_parties:
        raise ValueError("No parties pass the threshold. Adjust the threshold or verify data.")

    # Initialize seat columns for each party
    for party in eligible_parties:
        df[party + '_seats'] = 0

    # Seat allocation using D'Hondt method
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

        # Update seat allocation for the district
        for party, seat_count in results.items():
            df.loc[df[district_col] == district, party + '_seats'] = seat_count

    # Add total row
    total_row = pd.Series(index=df.columns)
    total_row[district_col] = str("Total")
    total_row[seats_col] = df[seats_col].sum()

    for party in eligible_parties:
        total_row[party] = df[party].sum()
        total_row[party + '_seats'] = df[party + '_seats'].sum()

    df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

    total_seats = {party: total_row[party + '_seats'] for party in eligible_parties}

    return {"totals": total_seats, "df_with_seats": df}
