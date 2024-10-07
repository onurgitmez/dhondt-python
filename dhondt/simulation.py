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
        A dictionary with three keys:
        - totals: A dictionary with each party's total seats.
        - df_with_seats: A DataFrame showing seats distribution across districts.
        - totals_df: A DataFrame showing total seats per party and vote counts.
    """

    # Fill NaN values in party columns with 0 (since no votes means no seats)
    df[parties] = df[parties].fillna(0)

    # Calculate total votes for all parties (ignore the threshold for vote totals)
    total_votes = df[parties].sum()

    # Apply the threshold only for seat allocation, not for vote counting
    vote_share = total_votes / total_votes.sum()
    eligible_parties = vote_share[vote_share >= threshold].index.tolist()

    # Initialize seat columns for each party (including those below the threshold)
    for party in parties:
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

        # Update seat allocations for eligible parties
        for party, seat_count in results.items():
            df.loc[df[district_col] == district, party + '_seats'] = seat_count

    # Create total row separately without inserting it into the main DataFrame
    total_row = pd.Series(index=df.columns)

    # Instead of using district_col for "Total", create a new column for labels
    total_row['label'] = "Total"

    # Sum up the total votes and seats for each party (including those below threshold)
    total_row[seats_col] = df[seats_col].sum()

    for party in parties:
        total_row[party] = df[party].sum()  # Include all votes
        total_row[party + '_seats'] = df[party + '_seats'].sum()  # Include only seat allocation for eligible parties

    # Create a separate DataFrame for the total row
    totals_df = pd.DataFrame([total_row])

    # Create a dictionary with total seats per party
    total_seats = {party: total_row[party + '_seats'] for party in parties}

    # Return the original DataFrame and the totals DataFrame separately
    return {"totals": total_seats, "df_with_seats": df, "totals_df": totals_df}
