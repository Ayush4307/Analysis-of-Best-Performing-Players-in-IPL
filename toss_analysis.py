import pandas as pd

def analyze_toss_impact(csv_path='matches.csv'):
    """
    Analyzes how winning the toss affects the probability of winning the match.
    """
    print("🏏 Starting Toss Impact Analysis...")
    
    try:
        matches = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
        return

    total_matches = len(matches)
    print(f"\nTotal Matches Analyzed: {total_matches}")

    # Calculate how many times the toss winner also won the match
    toss_winner_is_match_winner = matches[matches['toss_winner'] == matches['winner']]
    match_win_count = len(toss_winner_is_match_winner)
    
    win_percentage = (match_win_count / total_matches) * 100
    
    print(f"Matches where Toss Winner won the Match: {match_win_count}")
    print(f"Toss Win -> Match Win Percentage: {win_percentage:.2f}%\n")
    
    # Impact by decision (Bat vs Field)
    print("🎯 Impact by Toss Decision:")
    decision_impact = toss_winner_is_match_winner['toss_decision'].value_counts()
    for decision, count in decision_impact.items():
        total_decisions = len(matches[matches['toss_decision'] == decision])
        percentage = (count / total_decisions) * 100 if total_decisions > 0 else 0
        print(f"  - Decision to {decision.upper()}: Won {count} out of {total_decisions} times ({percentage:.2f}%)")

    # Export a summary file
    summary_df = matches.groupby(['venue', 'toss_decision']).apply(
        lambda x: pd.Series({
            'total_matches': len(x),
            'toss_and_match_wins': len(x[x['toss_winner'] == x['winner']])
        })
    ).reset_index()
    
    summary_df['win_percentage'] = (summary_df['toss_and_match_wins'] / summary_df['total_matches'] * 100).round(2)
    
    export_filename = 'toss_impact_summary.csv'
    summary_df.to_csv(export_filename, index=False)
    print(f"\n✅ Successfully exported detailed venue breakdown to {export_filename}")

if __name__ == "__main__":
    analyze_toss_impact()
