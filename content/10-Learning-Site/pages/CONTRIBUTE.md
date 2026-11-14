# Contribute

This site gets better when people who use it say what's wrong or missing. Everything comes in
through a short form on the Git Soma repository, so nothing gets lost.

## Three ways to help

| You want to… | Use | What happens next |
| --- | --- | --- |
| Report a mistake, a broken link or a confusing page | [Report a problem](https://git.soma.salesforce.com/akumthekar/claude-certifications-training/issues/new?template=report-a-problem.yml), or the link at the bottom of any page | Checked and fixed in the next update. Wrong facts are checked against Anthropic's docs first |
| Suggest a topic, lab, simulation or better explanation | [Request content](https://git.soma.salesforce.com/akumthekar/claude-certifications-training/issues/new?template=content-request.yml) | Added to the list and scheduled. Some ideas wait a few weeks |
| Share how your exam went | [Exam debrief](https://git.soma.salesforce.com/akumthekar/claude-certifications-training/issues/new?template=exam-debrief.yml) | Folded into [Insights](site:insights.html), anonymously unless you say otherwise |

You need to be signed in to Git Soma to open a form. Prefer Slack? Message the site owner (shown
on the repository page), and they'll send you the right form.

## What happens after you send a form

1. **Read and sorted**, about once a week: every issue gets a reply.
2. **Planned**: accepted issues go on the site's work list, and the issue says so. Fixes usually
   ship within two weeks; bigger ideas can take longer.
3. **Fixed and checked**: every change passes the site's review steps
   ([how this site is built](site:how-we-build.html)).
4. **Shipped**: the issue closes when the change is live, and it's listed on
   [What's new](site:whats-new.html). You're credited only if you agree.

Declined ideas get a short reason. Nothing is closed silently.

## The ground rules

- **No real exam questions or answers,** ever. The exams come with a confidentiality agreement.
- **Claude and Anthropic only.** Other companies' products and certifications are out of scope.
- **Facts need a source.** Anthropic's own docs and exam guides come first
  ([source tiers](site:about.html#source-tiers)).
- **Only share what you're allowed to share.** Don't paste someone else's course or question set
  without their permission.
- **Names stay private** unless you choose to be credited.

## Why there are no pull requests

The pages are generated from a source folder that isn't in the repository. A direct edit to the
repository would be overwritten on the next build, so changes come in as issues and are copied in
by hand. Design changes follow the [design style guide](site:style-guide.html).