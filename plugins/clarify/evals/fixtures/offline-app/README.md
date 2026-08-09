# fieldnotes

Note-taking for site surveyors. They write notes on a phone while walking a
site, then sync when they get back to the van. Coverage on site is bad and
often absent entirely.

Every note is a row in `notes`, fetched through React Query from the REST API
at `VITE_API_URL`. Photos upload separately and are referenced by id.
