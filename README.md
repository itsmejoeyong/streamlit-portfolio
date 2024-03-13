# blood-donation-pipeline-v2
Recently I've been more into the software development best practices, and In the second version I've significantly improved the overall readability of the codebase by implementing classes, abstracting & encapsulating a significant amount logic away from the main python file into its class & methods.

In this second interation I've built a more monolithic architecture, in which all infrastructure, tools & code resides in the virtual machine, as opposed to a more 'microservice' approach in the first iteration of the project.

---
### Workflow
![workflow](.drawio\workflow.png)

# Todo
- Additional churn/retention analysis on parquet file.
- setup cron job & bash script to refresh data.