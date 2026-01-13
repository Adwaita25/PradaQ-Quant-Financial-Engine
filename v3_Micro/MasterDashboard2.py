PAIRS_WATCHLIST = [
    {'a': 'HDFCBANK.NS', 'b': 'ICICIBANK.NS', 'sector': 'Banking'},
    {'a': 'RPOWER.BO', 'b': 'ADANIPOWER.NS', 'sector': 'Energy'},
    {'a': 'APOLLOHOSP.NS', 'b': 'CIPLA.NS', 'sector': 'HealthCare'},
    {'a': 'INFY.NS', 'b': 'HCLTECH.NS', 'sector': 'IT'},
    {'a': 'TATASTEEL.NS', 'b': 'JSWSTEEL.NS', 'sector': 'Mining'}
]


from IPython.display import clear_output

class MasterDashboard2:
    def update(self, pair_results, total_pnl):
        # Notebook-friendly clear
        clear_output(wait=True) 
        
        print(f"{'='*55}")
        print(f" PROJECT NEXUS: MULTI-PAIR PRODUCTION MONITOR ")
        print(f"{'='*55}")
        print(f"{'PAIR':<28} | {'Z-SCORE':<8} | {'POS':<8}")
        print(f"{'-'*55}")
        
        for p_id, data in pair_results.items():
            # Create a simple visual bar for each pair
            bar_pos = int((data['z'] + 3) / 6 * 20)
            bar_pos = max(0, min(20, bar_pos))
            bar = ["-"] * 21
            bar[10] = "|"
            bar[bar_pos] = "O"
            bar_str = "".join(bar)
            
            print(f"{p_id:<28} | {data['z']:>7.2f} | {data['pos']:<8}")
            print(f"  [{bar_str}]")
            
        print(f"{'-'*55}")
        print(f"TOTAL PORTFOLIO PNL: ₹{total_pnl:.2f}")
        print(f"{'='*55}")