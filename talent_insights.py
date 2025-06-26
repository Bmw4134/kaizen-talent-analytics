import os
import dash
from dash import dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import datetime
import logging

from kaizen_talent_analytics.services.model_orchestrator import ModelOrchestrator
from kaizen_talent_analytics.goal_tracker import GoalTracker, Goal
from kaizen_talent_analytics.session_audit import SessionLogger
from kaizen_talent_analytics.connectors.ats_adapter import load_ats_events, filter_events

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load dummy ATS data
try:
    ats_data = pd.read_csv("data/dummy_ats_events.csv")
except Exception as e:
    logger.error(f"Failed to load ATS data: {e}")
    ats_data = pd.DataFrame(columns=["candidate_id", "source", "stage", "outcome", "timestamp"])

# Initialize backend services
model_orchestrator = ModelOrchestrator()
goal_tracker = GoalTracker()
session_logger = SessionLogger()

# Add some stub goals for demo
goal_tracker.add_goal(Goal(id="G1", description="Improve sourcing channels", status="pending"))
goal_tracker.add_goal(Goal(id="G2", description="Reduce time to hire", status="completed"))
goal_tracker.add_goal(Goal(id="G3", description="Increase retention rate", status="failed"))

# Add some stub sessions for demo
session_logger.log_session(
    start_time=datetime.datetime.now().isoformat(),
    duration=3600,
    files_touched=["goal_tracker.py", "predictive_models.py"],
    active_modules=["RetentionModel", "GoalTracker"]
)
session_logger.log_session(
    start_time=(datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
    duration=1800,
    files_touched=["diff_tracker.py"],
    active_modules=["DiffWatcher"]
)

# Prepare funnel summary data
def prepare_funnel_data(df):
    stages_order = ['Sourced', 'Screened', 'Interview', 'Hired']
    counts = df['stage'].value_counts()
    data = []
    for stage in stages_order:
        data.append({'Stage': stage, 'Count': counts.get(stage, 0)})
    return pd.DataFrame(data)

funnel_data = prepare_funnel_data(ats_data)

# Initialize Dash app with Bootstrap theme
from flask import Flask, send_from_directory

server = Flask(__name__, static_folder='landing_page', static_url_path='')

app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.DARKLY])
app.title = "Kaizen Talent Insights: Netflix ML Application"

@server.route('/')
def serve_landing_page():
    return server.send_static_file('index.html')

# Helper function for color coding goal status
def color_code_status(status):
    return {
        "pending": "#fbbf24",    # yellow
        "completed": "#22c55e",  # green
        "failed": "#ef4444"      # red
    }.get(status, "#6b7280")     # gray default

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Kaizen Talent Insights: Netflix ML Application", className="mb-0"),
            html.P("Interactive Intelligence Dashboard for Hiring Funnel Optimization", className="lead"),
            html.Img(src="https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg",
                     style={"width": "100%", "borderRadius": "8px", "marginBottom": "20px"})
        ])
    ], className="mb-4"),

    # Grid layout for cards
    dbc.Row([
        # Funnel Summary
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Hiring Funnel Summary"),
                dbc.CardBody([
                    dcc.Graph(
                        id="funnel-chart",
                        figure=px.bar(funnel_data, x='Stage', y='Count', color='Stage',
                                      color_discrete_sequence=px.colors.qualitative.Dark24,
                                      labels={'Count': 'Number of Candidates', 'Stage': 'Hiring Stage'},
                                      title="Candidates at Each Hiring Stage")
                        .update_layout(plot_bgcolor='#222', paper_bgcolor='#222', font_color='white')
                    )
                ])
            ], className="mb-4")
        ], md=6),

        # Retention Forecast
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Retention Forecast"),
                dbc.CardBody([
                    dcc.Graph(id="retention-chart"),
                    html.P("This model predicts the likelihood of candidates remaining with the company over time. Scores closer to 1 indicate higher retention probability.",
                           className="text-muted")
                ])
            ], className="mb-4")
        ], md=6)
    ]),

    # Goal Tracker and Session Log
    dbc.Row([
        # Goal Tracker
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Goal Tracker"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id="goal-table",
                        columns=[
                            {"name": "Goal ID", "id": "id"},
                            {"name": "Description", "id": "description"},
                            {"name": "Status", "id": "status"},
                            {"name": "Last Updated", "id": "last_updated"},
                        ],
                        data=[],
                        style_cell={'backgroundColor': '#222', 'color': 'white', 'textAlign': 'left', 'padding': '8px'},
                        style_header={'backgroundColor': '#333', 'fontWeight': 'bold'},
                        style_data_conditional=[],
                        page_size=5,
                    )
                ])
            ], className="mb-4")
        ], md=6),

        # Session Log Viewer
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Session Log Timeline"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id="session-table",
                        columns=[
                            {"name": "Start Time", "id": "start_time"},
                            {"name": "Duration (s)", "id": "duration"},
                            {"name": "Files Touched", "id": "files_touched"},
                            {"name": "Active Modules", "id": "active_modules"},
                        ],
                        data=[],
                        style_cell={'backgroundColor': '#222', 'color': 'white', 'textAlign': 'left', 'padding': '8px'},
                        style_header={'backgroundColor': '#333', 'fontWeight': 'bold'},
                        page_size=5,
                    )
                ])
            ], className="mb-4")
        ], md=6)
    ]),

    # Hidden div for storing retention data to limit chart growth
    dcc.Store(id='retention-data-store', data=[])
], fluid=True)

# Callbacks
@app.callback(
    Output('retention-chart', 'figure'),
    Output('goal-table', 'data'),
    Output('goal-table', 'style_data_conditional'),
    Output('session-table', 'data'),
    Input('retention-data-store', 'data'),
    State('retention-data-store', 'data')
)
def update_dashboard(retention_data, retention_data_state):
    # Simulate retention predictions
    dummy_candidates = ['Alice', 'Bob', 'Charlie', 'Diana']
    dummy_scores = [0.85, 0.60, 0.75, 0.90]

    # Limit retention data history to last 10 entries to prevent infinite growth
    retention_data = retention_data[-10:] if retention_data else []
    new_entry = list(zip(dummy_candidates, dummy_scores))
    retention_data.append(new_entry)

    # Reset retention data if it grows beyond 50 entries to prevent memory bloat
    if len(retention_data) > 50:
        retention_data = retention_data[-10:]

    # Prepare retention chart data (latest entry)
    latest_data = retention_data[-1] if retention_data else []
    df_retention = pd.DataFrame(latest_data, columns=['Candidate', 'Retention Score'])

    retention_fig = px.bar(df_retention, x='Retention Score', y='Candidate', orientation='h',
                           labels={'Retention Score': 'Predicted Retention Score', 'Candidate': 'Candidate'},
                           title="Predicted Retention Scores")
    retention_fig.update_layout(plot_bgcolor='#222', paper_bgcolor='#222', font_color='white')

    # Prepare goal tracker data
    goals = list(goal_tracker._goals.values())
    goal_data = []
    style_conditional = []
    for g in goals:
        goal_data.append({
            "id": g.id,
            "description": g.description,
            "status": g.status,
            "last_updated": g.last_updated or "N/A"
        })
        style_conditional.append({
            'if': {'filter_query': f'{{status}} = "{g.status}"'},
            'backgroundColor': color_code_status(g.status),
            'color': '#000'
        })

    # Prepare session log data
    sessions = session_logger.get_sessions()
    session_data = []
    for s in sessions:
        session_data.append({
            "start_time": s.start_time,
            "duration": s.duration,
            "files_touched": ", ".join(s.files_touched),
            "active_modules": ", ".join(s.active_modules)
        })

    return retention_fig, goal_data, style_conditional, session_data

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8050))
    except ValueError:
        print("Invalid PORT environment variable. Falling back to port 8050.")
        port = 8050
    app.run(host="0.0.0.0", port=port)
