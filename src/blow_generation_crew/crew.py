from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
web_search_tool =  SerperDevTool()
@CrewBase
class BlowGenerationCrew():
    """BlowGenerationCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    tools = [web_search_tool]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def team_leader(self) -> Agent:
        return Agent(
            config=self.agents_config['team_leader'], # type: ignore[index]
            verbose=True,
            allow_delegation = True,
        )

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'], # type: ignore[index]
            verbose=True,
            allow_delegation = False,
            tools = self.tools,
        )

    @agent 
    def blog_writing_agent(self) ->Agent:
            return Agent(
                config=self.agents_config["blog_writing_agent"],
                verbose =True,
                allow_delegation = False,
            )
    
    @agent 
    def blog_review_agent(self) ->Agent:
            return Agent(
                config=self.agents_config["blog_review_agent"],
                verbose =True,
                allow_delegation = False,
            )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def blog_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_writing_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BlowGenerationCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents = [self.research_agent(),self.blog_writing_agent(),self.blog_review_agent()],
            tasks = [self.blog_writing_task()],
            process = Process.hierarchical,
            verbose = True,
            manager_agent = self.team_leader()
        )
