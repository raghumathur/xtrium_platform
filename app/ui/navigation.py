"""Navigation configuration for the application."""
from typing import Dict, List, Tuple

def get_tab_items() -> List[Tuple[str, str, str]]:
    """Get all available tabs."""
    return [
        ("home", "🏠", "Home"),
        ("discovery", "🔍", "Discovery"),
        ("sustainability", "🌱", "Sustainability"),
        ("supply_chain", "⛓️", "Supply Chain"),
        ("insights", "💡", "Insights"),
        ("assistance", "🤝", "Assistance")
    ]

def get_sidebar_links(active_tab: str) -> List[Tuple[str, str, str]]:
    """Get sidebar links for the active tab."""
    return SIDEBAR_LINKS.get(active_tab, [])

# Map of tab IDs to their sidebar links
SIDEBAR_LINKS: Dict[str, List[Tuple[str, str, str]]] = {
    "home": [
        ("Overview Metrics", "📊", "metrics"),
        (" Project Status", "📃", "projects"),
        (" Material and Application Insights", "🔍", "materials"),
        (" Sustainability", "🌱", "sustainability"),
        (" Activity", "🕒", "activity")
    ],
    "discovery": [
        ("Search Materials", "", "search_materials"),
        ("Browse Database", "", "browse_database"),
        ("Compare Materials", "", "compare_materials"),
        ("Saved Searches", "", "saved_searches")
    ],
    "sustainability": [
        ("Benchmarking & Goals", "🎯", "benchmarking"),
        ("Material Portfolio Analysis", "🧪", "material"),
        ("Enhanced Supply Chain", "🌐", "supply-chain")
    ],
    "supply_chain": [
        ("Discover Suppliers", "🏭", "suppliers"),
        ("Inventory Management", "📦", "inventory"),
        ("Cost Trend Analysis", "💰", "cost_analysis"),
        ("Supplier Risk Assessment", "⚠️", "risk_assessment")
    ],
    "insights": [
        ("Market Trends", "📈", "market_trends"),
        ("Industry Reports", "📑", "industry_reports"),
        ("Analytics", "📊", "analytics"),
        ("Forecasting", "🎯", "forecasting")
    ],
    "assistance": [
        ("Help Center", "❓", "help_center"),
        ("Documentation", "📚", "documentation"),
        ("Support Tickets", "🎫", "support_tickets"),
        ("Training", "🎓", "training")
    ]
}


