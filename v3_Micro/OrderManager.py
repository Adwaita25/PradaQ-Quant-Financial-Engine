import pandas as pd
import numpy as np

class OrderManager:
    """
    Handles Virtual Execution for Project PradaQ.
    Calculates share quantities  based on static beta to
    maintain Market-Neutral Position.
    """

    def __init__(self, capital, slippage_bps = 10):
        self.capital = capital
        self.slippage = slippage_bps / 10000
        self.position = 0 #1 for Long spread, -1 for Short, 0 for flat
        self.entry_spread = 0
        self.total_pnl = 0

    def calculate_quantities(self, price_a, price_b, beta):
        """
        Determines how many shares of A and B to trade.
        Formula: Qty_a = (Capital/2) / Price_A
                    Qty_b = (Qty_b * beta)   
        """

        #We split the capital 50/50 across the leg for simplicity
        qty_a = (self.capital / 2) // price_a
        qty_b = (qty_a * beta) // 1 # Maintain the hedge Ration
        return int(qty_a), int(qty_b)
        
    def execute_paper_trade(self, current_signal, price_a, price_b, beta, z_score):
        current_spread = price_a - (beta * price_b)
        
        # 1. EXIT: Calculate profit/loss when closing
        if self.position != 0 and ( (self.position == 1 and z_score >= 0) or (self.position == -1 and z_score <= 0) ):
            trade_pnl = (current_spread - self.entry_spread) * self.position
            self.total_pnl += trade_pnl
            self.position = 0
            return {"status": "closed", "pnl": trade_pnl}

        # 2. ENTRY: Record the spread price at entry
        if self.position == 0 and current_signal != 0:
            self.position = current_signal
            self.entry_spread = current_spread
            return {"status": "filled"}
            
        return None
