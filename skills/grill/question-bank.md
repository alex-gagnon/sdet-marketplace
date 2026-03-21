# Grill Question Bank

Question templates organized by concern domain. Select the domains most relevant to the proposal being challenged. Use these as starting points — adapt to the specific context.

## Scalability

- What happens at 10× the current load? Where does the first bottleneck appear?
- Where is the single point of failure? What happens when it goes down?
- What assumptions does this make about data volume that may not hold in 12 months?
- Is this design sharded? If not, how does it scale horizontally?
- What does the tail latency look like under load, not just average latency?

## Security

- Who is the attacker in this model? What do they want, and how might they get it?
- What can an authenticated-but-malicious user do that they shouldn't be able to?
- Where does user-supplied input touch a system boundary? Is it validated there?
- What happens if a dependency is compromised?
- What data is sensitive here, and who can read it?

## Assumptions

- What has to be true about the environment for this to work? Which of those can break?
- What is the cheapest way this fails? What's the most likely failure in production?
- What assumptions are you making about user behavior that users might not follow?
- What external service or team is this relying on? What's your plan if they change something?
- What would you have to believe to conclude this is the right approach?

## Alternatives

- What are the two most obvious alternative approaches? Why did you reject them?
- Has this been tried before in this codebase, company, or industry? What happened?
- What would the simplest possible version of this look like? Why do you need more?
- What would you do if you couldn't use [key technology/library/service]?
- If you were starting from scratch in 3 years with more knowledge, would you make the same choice?

## Dependencies

- What breaks immediately if [key dependency] is unavailable?
- Are there circular dependencies? What happens when you need to change one component?
- Who owns the downstream systems this touches? Do they know this depends on them?
- What version constraints are you accepting, and what happens when upstream moves?

## Reversibility

- If this turns out to be wrong, how do you undo it?
- What is the rollback plan in production?
- What decisions here are hard to reverse once made? Are you making them too early?
- If you ship this and it's wrong, how long until you know? How long to fix it?
- What data migrations are involved, and are they reversible?

## Operational Readiness

- How do you know this is working in production? What are you monitoring?
- What does an on-call engineer do at 3am when this breaks?
- What is the deployment strategy — big bang or incremental?
- Are there feature flags? Can you kill-switch this without a deploy?
- What does the runbook look like?
