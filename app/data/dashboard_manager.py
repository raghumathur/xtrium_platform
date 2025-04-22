import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

class DashboardDataManager:
    """Manager class for handling dashboard data operations."""
    
    def __init__(self):
        self.base_path = Path("assets/databases/dashboard")
    
    def _read_csv(self, filename: str) -> pd.DataFrame:
        """Read a CSV file from the dashboard database directory."""
        return pd.read_csv(self.base_path / filename)
    
    def get_project_data(self) -> pd.DataFrame:
        """Get project data for the dashboard."""
        return self._read_csv("projects.csv")
    
    def get_project_metrics(self) -> pd.DataFrame:
        """Get project metrics for the dashboard."""
        return self._read_csv("project_metrics.csv")
    
    def get_project_phases(self) -> pd.DataFrame:
        """Get project phases data."""
        return self._read_csv("project_phases.csv")
    
    def get_material_matches(self) -> pd.DataFrame:
        """Get material matches data."""
        return self._read_csv("material_matches.csv")
    
    def get_industry_data(self) -> pd.DataFrame:
        """Get industry analysis data."""
        return self._read_csv("industry_data.csv")
    
    def get_sustainability_trends(self) -> pd.DataFrame:
        """Get sustainability trends data."""
        df = self._read_csv("sustainability_trends.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    
    def get_recent_activities(self) -> pd.DataFrame:
        """Get recent activities data."""
        df = self._read_csv("recent_activities.csv")
        df['time'] = pd.to_datetime(df['time'])
        return df
    
    def get_metric_value(self, metric_name: str) -> tuple:
        """Get a specific metric value and its change.
        Returns:
            tuple: (value, change, change_type)
        """
        metrics = self._read_csv("project_metrics.csv")
        metric = metrics[metrics['Metric'] == metric_name].iloc[0]
        return metric['Value'], metric['Change'], metric['ChangeType']
    
    def get_sourcing_status(self) -> pd.DataFrame:
        """Get sourcing status data."""
        return self._read_csv("sourcing_status.csv")
    
    def get_sustainability_insights(self) -> pd.DataFrame:
        """Get sustainability insights data."""
        return self._read_csv("sustainability_insights.csv")
