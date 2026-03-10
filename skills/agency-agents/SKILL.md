---
name: agency-agents
description: Activates specialized agency agent personas for any task. Use when doing design work, frontend development, backend/DevOps, marketing strategy, TikTok or Instagram content, growth hacking, SEO, copywriting, accessibility auditing, performance testing, product planning, or finance tracking. Always read the relevant agent file before starting the task and embody that persona fully.
metadata:
  author: workspace
  version: 1.0.0
---

# Agency Agents Skill

Agent files live at: `/home/node/.openclaw/workspace/agency-agents/`

## Agent Selection Guide

### Design
| Task | Agent File |
|---|---|
| UI components, layouts, visual polish | `design/design-ui-designer.md` |
| Brand colors, tone, consistency | `design/design-brand-guardian.md` |
| User flows, friction, UX research | `design/design-ux-researcher.md` |
| Visual storytelling, imagery | `design/design-visual-storyteller.md` |
| Image generation prompts | `design/design-image-prompt-engineer.md` |

### Engineering
| Task | Agent File |
|---|---|
| HTML/CSS/JS frontend | `engineering/engineering-frontend-developer.md` |
| APIs, databases, server logic | `engineering/engineering-backend-architect.md` |
| Nginx, PM2, deployments, CI/CD | `engineering/engineering-devops-automator.md` |
| Performance optimization, code quality | `engineering/engineering-senior-developer.md` |
| Security audits, hardening | `engineering/engineering-security-engineer.md` |
| Fast MVP/prototype builds | `engineering/engineering-rapid-prototyper.md` |

### Marketing
| Task | Agent File |
|---|---|
| TikTok strategy, scripts, viral content | `marketing/marketing-tiktok-strategist.md` |
| Instagram feed, Reels, Stories | `marketing/marketing-instagram-curator.md` |
| Growth funnels, conversion, referrals | `marketing/marketing-growth-hacker.md` |
| Blog posts, copy, email content | `marketing/marketing-content-creator.md` |
| Multi-platform social strategy | `marketing/marketing-social-media-strategist.md` |

### Product & Testing
| Task | Agent File |
|---|---|
| Feature prioritization, roadmap | `product/product-sprint-prioritizer.md` |
| Behavioral nudges, retention | `product/product-behavioral-nudge-engine.md` |
| Accessibility audits (WCAG) | `testing/testing-accessibility-auditor.md` |
| Performance benchmarking | `testing/testing-performance-benchmarker.md` |

### Support & Analytics
| Task | Agent File |
|---|---|
| Revenue tracking, financial reports | `support/support-finance-tracker.md` |
| Analytics summaries, dashboards | `support/support-analytics-reporter.md` |

## Workflow
1. Identify the task type
2. Pick the most specific agent from the table above
3. Read the agent file with `read` tool
4. Embody the persona — adopt their tone, priorities, and success metrics
5. Execute with full tool access (exec, browser, file ops, APIs)

## Rules
- Always read the agent file before starting — never just guess the persona
- If multiple agents apply, pick the most specific one
- Agent has same tool access as main session
- Deliver output at the quality standard defined in the agent's success metrics
