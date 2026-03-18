# Stock Market System for Tycoon Game
# Dark mode with line graphs for stock price visualization

import tkinter as tk
from tkinter import ttk
import random
import math
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Dark mode colors
DARK_BG = "#1e1e1e"
DARK_FG = "#e0e0e0"
DARK_ACCENT = "#4a9eff"
DARK_SUCCESS = "#4caf50"
DARK_DANGER = "#f44336"
DARK_CARD = "#2d2d2d"
DARK_BORDER = "#404040"

# Different colors for each stock line
STOCK_COLORS = [
    "#ff6b6b",  # TECH - Red
    "#4ecdc4",  # ENGY - Teal
    "#ffe66d",  # BANK - Yellow
    "#95e1d3",  # MINR - Mint
    "#f38181",  # FOOD - Coral
    "#aa96da",  # AERO - Lavender
    "#fcbad3",  # HEAL - Pink
    "#a8d8ea",  # GAME - Light Blue
]

# Global gold reference
_gold_getter = None
_gold_setter = None

def set_gold_reference(g_get, g_set=None):
    """Set the reference to the game's gold variable"""
    global _gold_getter, _gold_setter
    _gold_getter = g_get
    if g_set:
        _gold_setter = g_set
    else:
        _gold_setter = lambda val: None

def get_gold():
    """Get current gold amount"""
    if _gold_getter is not None:
        return _gold_getter()
    return 0

def set_gold(amount):
    """Set gold amount"""
    if _gold_setter is not None:
        _gold_setter(amount)

# Stock data storage
class Stock:
    def __init__(self, symbol, name, base_price, volatility, color):
        self.symbol = symbol
        self.name = name
        self.price = base_price
        self.base_price = base_price
        self.volatility = volatility
        self.color = color
        self.price_history = [base_price] * 20
        self.shares_owned = 0
        
    def update_price(self):
        change_percent = random.uniform(-self.volatility, self.volatility)
        self.price *= (1 + change_percent)
        self.price = max(self.base_price * 0.1, min(self.base_price * 5, self.price))
        
        self.price_history.append(self.price)
        if len(self.price_history) > 50:
            self.price_history.pop(0)
    
    def get_change_percent(self):
        if len(self.price_history) < 2:
            return 0
        old_price = self.price_history[-2]
        if old_price == 0:
            return 0
        return ((self.price - old_price) / old_price) * 100


# Initialize stocks with colors
stocks = [
    Stock("MATH", "Jibrael's Calculus \nand Differentials \nInc.", 100, 0.08, STOCK_COLORS[0]),
    Stock("ENGY", "Fixed(?)Elec Inc.", 50, 0.05, STOCK_COLORS[1]),
    Stock("BANK", "Globally Defined Bank", 75, 0.03, STOCK_COLORS[2]),
    Stock("MINR", "CraftMiners Inc.", 200, 0.12, STOCK_COLORS[3]),
    Stock("FOOD", "BreadLine Ltd.", 30, 0.02, STOCK_COLORS[4]),
    Stock("AERO", "NineEleven Aviation", 150, 0.10, STOCK_COLORS[5]),
    Stock("HEAL", "Heal Station Atbp.", 80, 0.04, STOCK_COLORS[6]),
    Stock("GAME", "Bastijn's Ultimate\nPC Gaming Shop", 60, 0.15, STOCK_COLORS[7]),
]


def update_stock_prices():
    """Update all stock prices periodically"""
    for stock in stocks:
        stock.update_price()


def open_stock_market(root, g_get, g_set=None):
    """Open the stock market window"""
    global _gold_getter, _gold_setter
    _gold_getter = g_get
    if g_set:
        _gold_setter = g_set
    else:
        _gold_setter = lambda val: None
    
    market_win = tk.Toplevel(root)
    market_win.title("📈 Stock Market")
    market_win.geometry("1000x700")
    market_win.configure(bg=DARK_BG)
    market_win.attributes("-fullscreen", True)
    
    # Header
    header_frame = tk.Frame(market_win, bg=DARK_BG)
    header_frame.pack(fill="x", padx=20, pady=15)
    
    title_label = tk.Label(
        header_frame, 
        text="📈 STOCK MARKET", 
        font=("Cascadia Code", 28, "bold"),
        bg=DARK_BG, 
        fg=DARK_ACCENT
    )
    title_label.pack(side="left")
    
    # Gold display
    gold_label = tk.Label(
        header_frame,
        text=f"💰 {format(int(get_gold()))}G",
        font=("Cascadia Code", 22),
        bg=DARK_BG,
        fg=DARK_SUCCESS
    )
    gold_label.pack(side="right")
    
    def update_gold_display():
        gold_label.config(text=f"💰 {format(int(get_gold()))}G")
        market_win.after(200, update_gold_display)
    update_gold_display()
    
    # Close button
    close_btn = tk.Button(
        header_frame,
        text="✕ Close",
        font=("Cascadia Code", 14),
        bg=DARK_DANGER,
        fg="white",
        command=market_win.destroy,
        padx=15,
        pady=5
    )
    close_btn.pack(side="right", padx=20)
    
    # Redeem All button
    def redeem_all():
        total_value = 0
        for stock in stocks:
            if stock.shares_owned > 0:
                total_value += stock.price * stock.shares_owned
                stock.shares_owned = 0
        if total_value > 0:
            current_gold = get_gold()
            set_gold(current_gold + total_value)
            refresh_display()
    
    redeem_btn = tk.Button(
        header_frame,
        text="💰 Redeem All",
        font=("Cascadia Code", 14),
        bg="#9b59b6",
        fg="white",
        command=redeem_all,
        padx=15,
        pady=5
    )
    redeem_btn.pack(side="right", padx=10)
    
    # Main content area
    main_frame = tk.Frame(market_win, bg=DARK_BG)
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Left side - Stock list with buy/sell
    left_frame = tk.Frame(main_frame, bg=DARK_BG)
    left_frame.pack(side="left", fill="y", padx=(0, 10))
    
    tk.Label(
        left_frame,
        text="Your Portfolio",
        font=("Cascadia Code", 18, "bold"),
        bg=DARK_BG,
        fg=DARK_FG
    ).pack(pady=(0, 10))
    
    # Portfolio frame
    portfolio_frame = tk.Frame(left_frame, bg=DARK_CARD, bd=2, relief="solid")
    portfolio_frame.pack(fill="both", expand=True)
    
    # Portfolio total value display
    portfolio_total_frame = tk.Frame(left_frame, bg=DARK_BG)
    portfolio_total_frame.pack(fill="x", pady=(10, 5))
    
    portfolio_total_label = tk.Label(
        portfolio_total_frame,
        text="Total Portfolio: 0G",
        font=("Cascadia Code", 14, "bold"),
        bg=DARK_BG,
        fg=DARK_ACCENT
    )
    portfolio_total_label.pack()
    
    def update_portfolio_total():
        total = get_total_stock_value()
        portfolio_total_label.config(text=f"Total Portfolio: {format(int(total))}G")
        market_win.after(200, update_portfolio_total)
    update_portfolio_total()
    
    # Canvas for portfolio items
    portfolio_canvas = tk.Canvas(portfolio_frame, bg=DARK_CARD, highlightthickness=0)
    portfolio_scrollbar = ttk.Scrollbar(portfolio_frame, orient="vertical", command=portfolio_canvas.yview)
    portfolio_container = tk.Frame(portfolio_canvas, bg=DARK_CARD)
    
    portfolio_canvas.create_window((0, 0), window=portfolio_container, anchor="nw")
    portfolio_canvas.configure(yscrollcommand=portfolio_scrollbar.set)
    
    def on_portfolio_configure(event):
        portfolio_canvas.configure(scrollregion=portfolio_canvas.bbox("all"))
    portfolio_container.bind("<Configure>", on_portfolio_configure)
    
    portfolio_canvas.pack(side="left", fill="both", expand=True)
    portfolio_scrollbar.pack(side="right", fill="y")
    
    # Right side - Combined graph
    right_frame = tk.Frame(main_frame, bg=DARK_BG)
    right_frame.pack(side="right", fill="both", expand=True)
    
    # Graph title
    tk.Label(
        right_frame,
        text="📊 All Stocks Price History",
        font=("Cascadia Code", 18, "bold"),
        bg=DARK_BG,
        fg=DARK_FG
    ).pack(pady=(0, 10))
    
    # Combined graph frame
    graph_frame = tk.Frame(right_frame, bg=DARK_CARD, bd=2, relief="solid")
    graph_frame.pack(fill="both", expand=True, padx=(10, 0))
    
    # Create matplotlib figure once (will be updated, not recreated)
    fig = Figure(figsize=(8, 5), facecolor=DARK_CARD)
    ax = fig.add_subplot(111)
    
    # Set dark mode colors
    ax.set_facecolor(DARK_CARD)
    fig.patch.set_facecolor(DARK_CARD)
    ax.tick_params(colors=DARK_FG)
    for spine in ax.spines.values():
        spine.set_color(DARK_BORDER)
    ax.xaxis.label.set_color(DARK_FG)
    ax.yaxis.label.set_color(DARK_FG)
    ax.title.set_color(DARK_FG)
    
    # Create canvas once
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Store price labels for each stock
    price_labels = {}
    change_labels = {}
    
    # Create portfolio items
    portfolio_widgets = []
    
    def create_portfolio_item(stock):
        """Create a portfolio item widget"""
        item_frame = tk.Frame(portfolio_container, bg=DARK_CARD, bd=1, relief="solid")
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Symbol with color indicator
        color_indicator = tk.Label(
            item_frame,
            text="●",
            font=("Cascadia Code", 14),
            bg=DARK_CARD,
            fg=stock.color
        )
        color_indicator.pack(side="left", padx=(10, 5))
        
        tk.Label(
            item_frame,
            text=stock.symbol,
            font=("Cascadia Code", 14, "bold"),
            bg=DARK_CARD,
            fg=DARK_FG,
            width=6,
            anchor="w"
        ).pack(side="left", padx=5)
        
        # Company name under abbreviation
        tk.Label(
            item_frame,
            text=stock.name,
            font=("Cascadia Code", 9),
            bg=DARK_CARD,
            fg=DARK_FG,
            width=20,
            anchor="w"
        ).pack(side="left", padx=(0, 5))
        
        # Price and change
        price_frame = tk.Frame(item_frame, bg=DARK_CARD)
        price_frame.pack(side="left", padx=5)
        
        change = stock.get_change_percent()
        change_color = DARK_SUCCESS if change >= 0 else DARK_DANGER
        change_symbol = "▲" if change >= 0 else "▼"
        
        # Create price label and store reference
        price_label = tk.Label(
            price_frame,
            text=f"{format(int(stock.price))}G",
            font=("Cascadia Code", 12),
            bg=DARK_CARD,
            fg=DARK_FG,
            anchor="w"
        )
        price_label.pack(anchor="w")
        price_labels[stock.symbol] = price_label
        
        # Create change label and store reference
        change_label = tk.Label(
            price_frame,
            text=f"{change_symbol} {abs(change):.1f}%",
            font=("Cascadia Code", 10),
            bg=DARK_CARD,
            fg=change_color,
            anchor="w"
        )
        change_label.pack(anchor="w")
        change_labels[stock.symbol] = change_label
        
        # Shares owned and buttons
        shares_frame = tk.Frame(item_frame, bg=DARK_CARD)
        shares_frame.pack(side="right", padx=10)
        
        tk.Label(
            shares_frame,
            text=f"x{stock.shares_owned}",
            font=("Cascadia Code", 12),
            bg=DARK_CARD,
            fg=DARK_FG
        ).pack()
        
        # Buy/Sell buttons
        btn_frame = tk.Frame(item_frame, bg=DARK_CARD)
        btn_frame.pack(side="right", padx=5)
        
        def buy_stock(s=stock):
            current_gold = get_gold()
            if current_gold >= s.price:
                set_gold(current_gold - s.price)
                s.shares_owned += 1
                refresh_display()
        
        def sell_stock(s=stock):
            if s.shares_owned > 0:
                current_gold = get_gold()
                set_gold(current_gold + s.price)
                s.shares_owned -= 1
                refresh_display()
        
        # Store button references for state updates
        stock_buy_btn = None
        stock_sell_btn = None
        
        buy_btn = tk.Button(
            btn_frame,
            text="+",
            font=("Cascadia Code", 10, "bold"),
            bg=DARK_SUCCESS,
            fg="white",
            command=buy_stock,
            width=2,
            state=tk.NORMAL
        )
        buy_btn.pack(pady=2)
        stock_buy_btn = buy_btn
        
        sell_btn = tk.Button(
            btn_frame,
            text="-",
            font=("Cascadia Code", 10, "bold"),
            bg=DARK_DANGER,
            fg="white",
            command=sell_stock,
            width=2,
            state=tk.NORMAL
        )
        sell_btn.pack(pady=2)
        stock_sell_btn = sell_btn
        
        # Store button references in stock object for state updates
        stock.buy_btn = stock_buy_btn
        stock.sell_btn = stock_sell_btn
        
        return item_frame
    
    # Create all portfolio items
    for stock in stocks:
        create_portfolio_item(stock)
    
    # Function to update graph without flickering
    def update_graph():
        """Update the graph in place without recreating it"""
        ax.clear()
        
        # Set dark mode style
        ax.set_facecolor(DARK_CARD)
        for spine in ax.spines.values():
            spine.set_color(DARK_BORDER)
        ax.tick_params(colors=DARK_FG)
        ax.xaxis.label.set_color(DARK_FG)
        ax.yaxis.label.set_color(DARK_FG)
        ax.title.set_color(DARK_FG)
        
        # Plot all stocks
        x_data = list(range(50))
        
        for i, stock in enumerate(stocks):
            # Normalize prices to show relative change (percentage from start)
            if len(stock.price_history) > 0:
                base = stock.price_history[0]
                if base > 0:
                    normalized = [(p / base - 1) * 100 for p in stock.price_history]
                    ax.plot(x_data[-len(normalized):], normalized, 
                           color=stock.color, linewidth=2, label=stock.symbol, alpha=0.8)
        
        ax.set_title("All Stocks Price History (% Change)", color=DARK_FG, fontsize=14, pad=10)
        ax.set_xlabel("Time", color=DARK_FG)
        ax.set_ylabel("% Change", color=DARK_FG)
        ax.grid(True, alpha=0.2, color=DARK_BORDER)
        ax.legend(loc='upper left', facecolor=DARK_CARD, edgecolor=DARK_BORDER, 
                 labelcolor=DARK_FG, fontsize=10)
        
        # Redraw the canvas
        canvas.draw()
    
    # Function to update button states
    def update_button_states():
        """Update button states based on gold and shares"""
        current_gold = get_gold()
        for stock in stocks:
            if hasattr(stock, 'buy_btn') and stock.buy_btn:
                try:
                    if current_gold < stock.price:
                        stock.buy_btn.config(state=tk.DISABLED, bg="#555555")
                    else:
                        stock.buy_btn.config(state=tk.NORMAL, bg=DARK_SUCCESS)
                except:
                    pass
            
            if hasattr(stock, 'sell_btn') and stock.sell_btn:
                try:
                    if stock.shares_owned <= 0:
                        stock.sell_btn.config(state=tk.DISABLED, bg="#555555")
                    else:
                        stock.sell_btn.config(state=tk.NORMAL, bg=DARK_DANGER)
                except:
                    pass
    
    # Function to refresh display
    def refresh_display():
        """Refresh portfolio items and update graph"""
        # Clear and recreate portfolio
        for widget in portfolio_container.winfo_children():
            widget.destroy()
        
        for stock in stocks:
            create_portfolio_item(stock)
        
        # Update button states based on gold and shares
        current_gold = get_gold()
        for stock in stocks:
            if hasattr(stock, 'buy_btn') and stock.buy_btn:
                if current_gold < stock.price:
                    stock.buy_btn.config(state=tk.DISABLED, bg="#555555")
                else:
                    stock.buy_btn.config(state=tk.NORMAL, bg=DARK_SUCCESS)
            
            if hasattr(stock, 'sell_btn') and stock.sell_btn:
                if stock.shares_owned <= 0:
                    stock.sell_btn.config(state=tk.DISABLED, bg="#555555")
                else:
                    stock.sell_btn.config(state=tk.NORMAL, bg=DARK_DANGER)
        
        # Update graph without recreating
        update_graph()
    
    # Initial graph draw
    update_graph()
    
    # Price update function - only updates graph, doesn't rebuild widgets
    def refresh_prices():
        """Refresh stock prices"""
        try:
            update_stock_prices()
            
            # Update button states (enable/disable based on gold and shares)
            update_button_states()
            
            # Update portfolio prices without rebuilding
            update_portfolio_prices()
            
            # Only update the graph, not the whole UI
            update_graph()
        except Exception as e:
            print(f"Error refreshing prices: {e}")
        
        # Schedule next update
        market_win.after(3000, refresh_prices)
    
    # Function to update portfolio price displays without rebuilding
    def update_portfolio_prices():
        """Update the price labels in the portfolio without rebuilding widgets"""
        for stock in stocks:
            if stock.symbol in price_labels:
                try:
                    # Update price label
                    price_labels[stock.symbol].config(text=f"{format(int(stock.price))}G")
                    
                    # Update change label
                    change = stock.get_change_percent()
                    change_color = DARK_SUCCESS if change >= 0 else DARK_DANGER
                    change_symbol = "▲" if change >= 0 else "▼"
                    change_labels[stock.symbol].config(
                        text=f"{change_symbol} {abs(change):.1f}%",
                        fg=change_color
                    )
                except:
                    pass
    
    # Start price updates
    refresh_prices()
    
    # Handle window close
    def on_close():
        market_win.destroy()
    market_win.protocol("WM_DELETE_WINDOW", on_close)


def get_total_stock_value():
    """Calculate total value of all stocks owned"""
    total = 0
    for stock in stocks:
        total += stock.price * stock.shares_owned
    return total


def get_total_shares_owned():
    """Get total number of shares owned"""
    total = 0
    for stock in stocks:
        total += stock.shares_owned
    return total
