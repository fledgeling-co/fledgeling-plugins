export const meta = {
  name: 'motion-film-corpus',
  description: 'One headless Sonnet 5.5 worker per SaaS marketing film: transcript via router MCP, download, 1 frame per 2 s, be-my-witness looking, validated findings.json',
  phases: [{ title: 'Analyse', detail: '48 films, 6 at a time, longest first; each launcher starts and waits on one Sonnet worker' }],
}

const FILMS = args.films
const CONC = args.concurrency || 6
const TOOLS = '~/Movies/motion-craft-corpus/tools'

const STATUS = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    state: { type: 'string', enum: ['done', 'failed'] },
    findings_status: { type: 'string' },
    validator: { type: 'string' },
    cost_usd: { type: 'number' },
    frames_read: { type: 'integer' },
    frames_expected: { type: 'integer' },
    strips_read: { type: 'integer' },
    be_my_witness_invoked: { type: 'boolean' },
    transcript_mcp_calls: { type: 'integer' },
    attempts: { type: 'integer' },
  },
  required: ['id', 'state', 'validator', 'attempts'],
}

function launcherPrompt(f) {
  return `You launch and wait on one headless analysis worker for the YouTube film ${f.id} (${f.brand}, ${f.duration} s). The worker is a separate Claude Sonnet process that does the analysis; you do not analyse the film yourself.

1. Run \`bash ${TOOLS}/run-worker.sh ${f.id}\` with a Bash timeout of 60000 ms. It prints one JSON line.
2. Run \`bash ${TOOLS}/wait-worker.sh ${f.id} 560\` with a Bash timeout of 600000 ms. It blocks for up to 560 s and prints one JSON line with a "state" field. Repeat this command while the state is "running" or "starting", up to 9 times in total.
3. If the state is "failed", run step 1 once more, then repeat step 2 up to 9 more times. Count the attempts: 1, or 2 when you relaunched.
4. If the state is still "running" after the last wait, return state "failed" with validator "launcher stopped waiting; worker still running".

Return these fields, taken from the last status line: id, state ("done" or "failed"), findings_status (the string "none" when it is null or absent), validator, attempts, and from its "audit" object cost_usd, frames_read, frames_expected, strips_read, be_my_witness_invoked and transcript_mcp_calls. Use -1, false or "none" for a field the line does not carry.

Run no other commands, read no other files and edit nothing. If one of the two scripts errors, run it once more; if it errors again, return state "failed" with the error text as validator. A status line that says "running" is not a finish: keep waiting until it says "done" or "failed", or until the wait limit above.`
}

async function pool(items, n, fn) {
  const results = new Array(items.length)
  let next = 0
  async function worker() {
    while (next < items.length) {
      const idx = next++
      try { results[idx] = await fn(items[idx], idx) } catch (e) { results[idx] = null }
    }
  }
  await Promise.all(Array.from({ length: Math.min(n, items.length) }, worker))
  return results
}

phase('Analyse')
log(`${FILMS.length} films, ${CONC} concurrent launchers`)
const results = await pool(FILMS, CONC, async (f, i) => {
  const label = `${f.brand} ${f.id} ${f.duration}s`
  let r = await agent(launcherPrompt(f), { label, phase: 'Analyse', schema: STATUS, effort: 'low' })
  if (!r) r = await agent(launcherPrompt(f), { label: label + ' (retry)', phase: 'Analyse', schema: STATUS, effort: 'low' })
  const out = r || { id: f.id, state: 'failed', validator: 'launcher agent returned nothing twice', attempts: 0 }
  log(`${out.state === 'done' ? 'done' : 'FAILED'} ${f.id} ${f.brand} frames ${out.frames_read}/${out.frames_expected} $${out.cost_usd}`)
  return out
})
const done = results.filter(r => r && r.state === 'done')
const failed = results.filter(r => !r || r.state !== 'done')
log(`${done.length}/${FILMS.length} done, ${failed.length} failed`)
return { done: done.length, failed: failed.map(r => r ? { id: r.id, validator: r.validator } : null), results }
