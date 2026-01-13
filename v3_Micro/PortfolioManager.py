from v3_Micro.OrderManager import OrderManager

class PortfolioManager:
    """
    Manages multiple pairs simultaneously.
    Acts as 'Fund Manager' for Project PradaQ.
    """

    def __init__(self, pairs_config, total_capital = 10000000):
        self.pairs = pairs_config   # List of dicts: {'a': HDFC, 'b': ICICI, 'beta': 0.17}
        self.total_capital = total_capital
        self.managers = {f"{p['a']}_{p['b']}": OrderManager(capital=total_capital/len(pairs_config))
                         for p in self.pairs}
        self.total_pnl = 0

    def update_portfolio(self, current_data_row, anchor_stats):
        """
        Updates every pair in the portfolio for a single tick
        """
        session_pnl = 0
        for pair in self.pairs:
            pair_id = f"{pair['a']}_{pair['b']}"
            p_a, p_b = current_data_row[pair['a']], current_data_row[pair['b']]
            
            # Calculate Z for this specific pair
            stats = anchor_stats[pair_id]
            spread = p_a - (pair['beta'] * p_b)
            z = (spread - stats['mean']) / stats['std']

            # Execute trade via specific pairs' manager
            signal = 0
            if z > 1.0: signal = -1
            elif z < -1.0: signal = 1

            self.managers[pair_id].execute_paper_trade(signal, p_a, p_b, pair['beta'], z)
            session_pnl += self.managers[pair_id].total_pnl
        
        self.total_pnl = session_pnl

