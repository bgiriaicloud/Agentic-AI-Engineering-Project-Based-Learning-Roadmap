from typing import TypedDict, Optional

class MigrationState(TypedDict):
    """
    Represents the shared memory state of the LangGraph workflow.
    This dict is modified as different specialized agents run.
    """
    user_query: str
    infrastructure_plan: Optional[str]
    cost_review: Optional[str]
    security_compliance_review: Optional[str]
    current_step: str
    revisions_count: int
    final_report: Optional[str]
