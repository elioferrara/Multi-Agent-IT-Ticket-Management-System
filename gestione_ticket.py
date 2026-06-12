# Librerie Agno
from agno.os import AgentOS

# Librerie personali
from agents.technical_team_leader import technical_team_leader
from agents.retain_agent import retain_agent
from agents.editor_agent import research_workflow
from agents.technical_agent import technical_agent
from agents.security_agent import security_agent
from agents.technical_human import technical_human
from agents.compliance_agent import compliance_agent
from database.database import db



agent_os = AgentOS(
    name="technical_support_os",
    agents=[technical_team_leader, retain_agent, technical_agent, technical_human, security_agent, compliance_agent],
    workflows=[research_workflow],
    db=db,
    tracing=True,
)

app = agent_os.get_app()