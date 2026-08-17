# The corpus — Google's own words, verbatim

Every `[docs]` claim a `gemini.md` makes is checked against this file by
`scripts/verify_quotes.py`, so what is here is reproduced **exactly** as Google
published it. Quote from this file; do not paraphrase inside quotation marks.

The full consolidated material — fifteen sources, gathered 17 August 2026 — is
carried by the `gemini-prompt-engineering` skill. What follows are the passages
this skill's guidance actually rests on, grouped by the module that uses them.
Sources: the Gemini API prompt-design-strategies page, the Gemini Enterprise
Agent Platform pages (prompt design, system instructions, multimodal prompts,
generation parameters, thinking, thinking prompting guide), the Google Cloud
prompt-engineering overview, and the Gemini 3.7 Flash model card.

---

## Core: verbosity, ambiguity, and one pass doing too much

> By default, Gemini 3 models provide direct and efficient answers. If you need a more conversational or detailed response, you must explicitly request it in your instructions.

> Be precise and direct: State your goal clearly and concisely. Avoid unnecessary or overly persuasive language.

> Define parameters: Explicitly explain any ambiguous terms or parameters.

From the prompt health checklist, under **Ambiguity**:

> Avoid using subjective or relative qualifiers that lack a concrete, measurable definition. Instead, provide objective constraints (for example, "write a summary of 3 sentences or less" instead of "write a brief summary").

Under **Clarity**:

> If you find yourself wondering about the scope, the specific steps to take, or the implicit assumptions being made, the prompt is likely unclear.

Under **Too many tasks**:

> If the prompt asks the model to perform several distinct cognitive actions in a single pass (for example, 1. Summarize, 2. Extract entities, 3. Translate, and 4. Draft an email), it is likely trying to accomplish too much. Break the requests into separate prompts.

Under **Underspecified task**:

> Ensure that the prompt's instructions provide a clear path for handling edge cases and unexpected inputs, and provide instructions for handling missing data rather than assuming inserted data will always be present and well-formed.

Under **Conflicting internal references**:

> Avoid writing a prompt with non-linear logic or conditionals that require the model to piece together fragmented instructions from multiple different places in the prompt.

The remedy for an overloaded pass, from "Break down prompts into components":

> Chain prompts: For complex tasks that involve multiple sequential steps, make each step a prompt and chain the prompts together in a sequence. In this sequential chain of prompts, the output of one prompt in the sequence becomes the input of the next prompt. The output of the last prompt in the sequence is the final output.

---

## Core: verification has to be asked for

From the thinking prompting guide, under "Verification and reflection":

> Include specific verification steps in either the system instructions or your prompts directly. For example, ask Gemini to verify its sources, review its reasoning, identify potential errors, and check its final answer.

From the agentic system-instruction template — two of its nine numbered rules:

> Review your output against the user's task.

> Verify your claims by quoting the exact applicable information (including policies) when referring to them.

And its last rule, on acting before the reasoning is done:

> Inhibit your response: only take an action after all the above reasoning is completed. Once you've taken an action, you cannot take it back.

---

## Core: the retry ceiling

From the same template, rule 8.2:

> This persistence must be intelligent: On *transient* errors (e.g. please try again), you *must* retry **unless an explicit retry limit (e.g., max x tries) has been reached**. If such a limit is hit, you *must* stop. On *other* errors, you must change your strategy or arguments, not repeat the same failed call.

---

## Core: few-shot is the strongest single lever

> We recommend to always include few-shot examples in your prompts. Prompts without few-shot examples are likely to be less effective. In fact, you can remove instructions from your prompt if your examples are clear enough in showing the task at hand.

> Make sure that the structure and formatting of few-shot examples are the same to avoid responses with undesired formats.

> Models like Gemini can often pick up on patterns using a few examples, though you may need to experiment with the number of examples to provide in the prompt for the best results. At the same time, if you include too many examples, the model may start to overfit the response to the examples.

From the health checklist, under **Missing output format specification**:

> Missing output format specification: Avoid leaving the model to guess the structure of the output; instead, use a clear, explicit instruction to specify the format and show the output structure in your few-shot examples.

---

## Core: thinking is internal, so don't ask for narration

> Gemini 2.5 and 3 series models automatically generate internal "thinking" text to improve reasoning performance. As such, it's generally not necessary to have the model outline, plan, or detail reasoning steps in the returned response itself. For problems that require heavy reasoning, simple requests like "Think very hard before answering" can improve performance, though at the cost of extra thinking tokens.

From the health checklist, under **Thinking vs. Reasoning**:

> If you're using Thinking, try prompting without step-by-step instructions on how the model should reason through the task. Rather, test relying on Thinking, and see if the step-by-step reasoning Thinking generates improves performance over your explicit step-by-step reasoning instructions.

On `thinking_level`, which the caller may control:

> HIGH: Allows the model to use more tokens for thinking and is suitable for complex prompts requiring deep reasoning, such as multi-step planning, verified code generation, or advanced function calling scenarios.

Defaults, from the same table: Gemini 3.7 Flash `MEDIUM`; 3.6 Flash `MEDIUM`;
3.5 Flash `MEDIUM`; 3.5 Flash-Lite `MINIMAL`; 3.1 Pro preview `HIGH`;
3 Flash preview `HIGH`.

On sampling parameters:

> Although you can modify these parameters, we strongly recommend keeping them at their default values for Gemini 3.x models. Changing these parameters (for example, setting the temperature below 1.0) can cause unexpected behavior, such as looping or degraded performance, particularly in complex mathematical or reasoning tasks.

---

## Core: structure, and where the instruction goes

> Use consistent structure: Employ clear delimiters to separate different parts of your prompt. XML-style tags (e.g., `<context>`, `<task>`) or Markdown headings are effective. Choose one format and use it consistently within a single prompt.

> Prioritize critical instructions: Place essential behavioral constraints, role definitions (persona), and output format requirements in the System Instruction or at the very beginning of the user prompt.

> Structure for long contexts: When providing large amounts of context (e.g., documents, code), supply all the context first. Place your specific instructions or questions at the very *end* of the prompt.

> Anchor context: After a large block of data, use a clear transition phrase to bridge the context and your query, such as "Based on the information above..."

---

## Module `emphasis`: escalating language stopped working

From the health checklist, under **Overt manipulation**:

> Remove language outside of the core task from the prompt that attempts to influence performance using emotional appeals, flattery, or artificial pressure. While first generation foundation models showed improvement in some circumstances with instructions like "very bad things will happen if you don't get this correct", foundation model performance will no longer improve and in many cases will get worse.

---

## Module `visual`: describe the image before judging it

> Ask the model to describe the images before performing the task in the prompt.

The worked example, where a generic instruction returns a generic caption:

> Describe this image.

returns *"The image shows an airport arrivals and departures board"*, whereas

> Parse the time and city from the airport board shown in this image into a list.

returns the thirteen rows. Two further instructions from the same page:

> To improve the response, point out which parts of the image are most relevant to the prompt.

> A prompt can fail because the model did not understand the image at all, or because it did not perform the correct reasoning steps afterward. To disambiguate between those reasons, ask the model to describe what's in the image.

> Handle multimodal inputs coherently: When using text, images, audio, or video, treat them as equal-class inputs. Ensure your instructions clearly reference each modality as needed.

> For complex tasks like those that require both visual understanding and reasoning, split the task into smaller, more straightforward steps or directly ask the model to think step by step in the prompt.

---

## Module `platform-values`: recall is not a source

> Your knowledge cutoff date is January 2025.

From the Gemini 3.7 Flash model card:

> The knowledge cutoff date for Gemini 3.7 Flash is March 2026 — users can expect updated information for some domains while in others they may experience the model's knowledge is limited to January 2025 (in line with the Gemini 3 Model Family).

The system-instruction clause Google supplies for time-sensitive work:

> For time-sensitive user queries that require up-to-date information, you MUST follow the provided current time (date and year) when formulating search queries in tool calls. Remember it is 2026 this year.

On grounding as the remedy:

> Grounding with Google Search connects the Gemini model to real-time web content, and should be enabled whenever the model may need to know obscure or recent facts.

> Reduces model hallucinations, instances where the model generates content that isn't factual.

---

## Module `authorship`: the strictly-grounded system instruction

Reproduced in full, because it is meant to be used verbatim:

> You are a strictly grounded assistant limited to the information provided in the User Context. In your answers, rely **only** on the facts that are directly mentioned in that context. You must **not** access or utilize your own knowledge or common sense to answer. Do not assume or infer from the provided facts; simply report them exactly as they appear. Your answer must be factual and fully truthful to the provided text, leaving absolutely no room for speculation or interpretation. Treat the provided context as the absolute limit of truth; any facts or details that are not directly mentioned in the context must be considered **completely untruthful** and **completely unsupported**. If the exact answer is not explicitly written in the context, you must state that the information is not available.

---

## Module `injection`: untrusted input needs a delimiter and a guard

From the health checklist, under **Prompt injection risk**:

> Check if there are explicit safeguards surrounding untrusted user input that is inserted into the prompt, as this can be a major security risk.

The mechanism, from Google's structured-prompt template — the comment is theirs:

> `[Insert User Input Here - The model knows this is data, not instructions]`

---

## Module `delegation` and closed sets: reframe as multiple choice

From the prompt iteration strategies, on a model that answered correctly but
outside the offered options:

> The response is correct, but the model didn't stay within the bounds of the options. You also want the model to just respond with one of the options instead of in a full sentence. In this case, you can rephrase the instructions as a multiple choice question and ask the model to choose an option.

And on when an agent may act without checking in, from the agentic template's
risk-assessment rule:

> For exploratory tasks (like searches), missing *optional* parameters is a LOW risk. **Prefer calling the tool with the available information over asking the user, unless** your `Rule 1` (Logical Dependencies) reasoning determines that optional information is required for a later step in your plan.

---

## Module `gate`: format and machine-readability

From the health checklist, under **Non-standard data format**:

> When model outputs must be machine-readable or follow a specific format, use a widely recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries.

Under **Task outside of model capabilities**:

> Avoid using prompts that ask the model to perform a task for which it has a known, fundamental limitation.

Under **Incorrect Chain of Thought (CoT) order**:

> Avoid providing examples that show the model generating its final, structured answer before it has completed its step-by-step reasoning.

And on arithmetic, which a gate often needs:

> Gemini's code execution tool enables the model to generate and run Python code, and should be enabled whenever the model needs to perform any kind of arithmetic, counting, or calculation.

---

## One caution about this file

Google's own pages disagree with each other in places, and the disagreements are
reproduced rather than resolved: the multimodal page recommends starting
temperature at `0.4`, the Agent Platform parameters page recommends `1.0`, and
the Gemini 3.x note says to leave sampling parameters alone entirely. Where a
`gemini.md` needs one of these, cite which page it came from.
