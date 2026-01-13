# v3_Production/Portfolio_Config.py

PAIRS_WATCHLIST = [
    {'a': 'HDFCBANK.NS', 'b': 'ICICIBANK.NS', 'sector': 'Banking'},
    {'a': 'IOC.NS', 'b': 'ONGC.NS', 'sector': 'Energy'},
    {'a': 'SBIN.NS', 'b': 'BANKBARODA.NS', 'sector': 'Banking'}
]

import sys

class MasterDashboard:
    def update(self, pair_results, total_pnl):
        # Clear screen (standard terminal trick)
        sys.stdout.write("\033[H\033[J") 
        
        print(f"{'='*50}")
        print(f" PROJECT PradaQ: MULTI-PAIR PRODUCTION MONITOR ")
        print(f"{'='*50}")
        print(f"{'PAIR':<25} | {'Z-SCORE':<8} | {'POS':<8}")
        print(f"{'-'*50}")
        
        for p_id, data in pair_results.items():
            # Create a simple visual bar for each pair
            bar_pos = int((data['z'] + 3) / 6 * 20)
            bar_pos = max(0, min(20, bar_pos))
            bar = ["-"] * 21
            bar[10] = "|"
            bar[bar_pos] = "O"
            bar_str = "".join(bar)
            
            print(f"{p_id:<25} | {data['z']:>7.2f} | {data['pos']:<8}")
            print(f"  [{bar_str}]")
            
        print(f"{'-'*50}")
        print(f"TOTAL PORTFOLIO PNL: ₹{total_pnl:.2f}")
        print(f"{'='*50}")
        sys.stdout.flush()