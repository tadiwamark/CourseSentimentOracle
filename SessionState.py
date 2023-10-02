import streamlit.ReportThread as ReportThread
from streamlit.server.Server import Server


class _SessionState:
    def __init__(self, **kwargs):
        """Initialize SessionState with default values."""
        for key, val in kwargs.items():
            setattr(self, key, val)


def get(**kwargs):
    """Get the Session State and set initial values."""
    session_id = ReportThread.get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    if not hasattr(session_info, "_session_state"):
        setattr(session_info, "_session_state", _SessionState(**kwargs))

    return session_info._session_state
