# Lighter

Lighter is an AI agent suite built around one idea: most tasks don't need the biggest model you have.

The usual setup throws every request at a large model with a long system prompt and a pile of tool definitions attached. That works, but you pay for it in tokens, latency, and compute — even when the question was "what's 12% of 340?" Lighter spends only what the task actually costs: short prompts, minimal context, few tools, and the smallest model that can still do the job.

Everything runs locally through [Ollama](https://ollama.com). No API keys, no per-token bill.

## The pieces

**Router.** Every query gets sized before it gets answered. Lighter estimates the context it needs, checks what the task actually requires — reasoning, tool use, long-form generation — and picks the smallest installed model that clears the bar. A one-line question goes to a 1B model. A multi-step research task escalates. You don't pick the model; you just ask.

**Agents.** Narrow on purpose. A research agent (more coming soon) — each with its own small prompt and only the tools it actually uses. A general-purpose agent has to carry every tool definition into every call. A narrow one doesn't, and that's most of the savings.

**Conversation storage.** History lives on disk, not in the prompt. Older turns get summarized and only the relevant slice comes back for the next request, so a long conversation doesn't turn into a linearly growing bill. Sessions survive restarts.

**Benchmarks.** The part that makes the rest credible. A harness that runs the same task set through Lighter and through an always-use-the-big-model baseline, then reports tokens, latency, wall-clock, estimated cost, and answer quality side by side. Efficiency claims without numbers are just vibes, so the numbers ship with the project.

## Using it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```

An interactive prompt. Type a question, get an answer, and see which model handled it and what it cost.

```
> summarize the notes in ~/meetings from this week
[llama3.2:1b · 412 tok · 0.8s]
...
```

Benchmarks run separately:

```bash
python -m bench --suite core --baseline llama3.1:70b
```

## Design notes

A few things Lighter is opinionated about:

- **Smallest model that works, not the best model available.** Escalate when a task demands it; don't start there.
- **Context is a budget.** Anything in the prompt should have earned its place.
- **Tools are expensive before they're ever called.** Their definitions cost tokens on every request, so agents carry few.
- **Measure it or don't claim it.** Every efficiency decision should be visible in the benchmark output.

## What's built, what isn't

**Working**

- [x] Model discovery — reads installed Ollama models, parses parameter size and context length
- [x] Query sizing — heuristic token estimate mapped to a required context window
- [x] Model selection — sorts smallest-first, picks the first model that fits
- [x] Single-shot query execution against the selected model
- [x] Interactive REPL (`main.py`)

**Left to do**

*Router*
- [ ] Read context length for non-Llama architectures (currently hardcoded to `llama.context_length`)
- [ ] Replace the character heuristic with real tokenization
- [ ] Route on task type, not just size — reasoning, tool use, and long generation need capability checks
- [ ] Escalation path: retry on a larger model when the small one fails or low-confidences
- [ ] Sensible fallback when no installed model fits

*Agents*
- [ ] Agent base class — prompt, tool set, execution loop
- [ ] Research agent (`src/agents/research-agent.py` is still empty)
- [ ] Tool calling, with per-agent tool sets so definitions don't ride along on every request

*Conversation storage*
- [ ] Persist sessions to disk
- [ ] Summarize and compress older turns
- [ ] Retrieve only the relevant slice into the next prompt

*Benchmarks*
- [ ] Task suite with expected outputs
- [ ] Baseline runner (always-use-the-big-model, for comparison)
- [ ] Metrics: tokens, latency, wall-clock, estimated cost
- [ ] Answer-quality scoring, so savings can be weighed against accuracy
- [ ] Reported results in this README

*Plumbing*
- [ ] `requirements.txt` (currently just `ollama`)
- [ ] Error handling — Ollama not running, no models installed, model load failure
- [ ] Per-query telemetry line (model, tokens, time)
- [ ] CLI flags: one-shot mode, model override, verbosity
- [ ] Tests
- [ ] Clean exit from the REPL

Interfaces will move around until the benchmark harness exists — that's the milestone that makes the rest of the claims checkable.

## License

MIT — see [LICENSE](LICENSE).
