# tour_recomendation_from_pdfs

# Introduction
A short project for learning about AI engineering based on using multi-source retrieval with attribution.

# Brief description
1. Several city tour pdfs were downloaded and saved locally.
2. Textual information extracted, chunked with a constant character length and constant overlap.
3. The chunks saved in a persistent Chroma database (saved locally) with the metadata to track the source.
4. Relevant information obtained from the database
5. Prompt constructing using the relevant information and its source
6. LLM given the prompt and asked the question, returning answers and source information.

# Obvious improvements
1. Query from the database should always be related to the question asked by the user.
2. Database query could be adjusted based on the user question using LLM. A few variations may be needed to get better context.
3. Text extraction and chunking are rudimentary and could be easily improved.
4. SAFETY - last but not least. There are no safety measures.
5. Checks - there are not formal checks to ensure that the code is running well.

# Personal take 2026-03-14
1. Turned out to be a quite similar project to the one recently done, so worked good as a review but also there were some new elements.
2. It is fun that the available tools, APIs and help from the AI coding assistants, allow not only to build working products quickly but to get explanations from different angles of why things works or why they don't work, what are alternative options and why one option is prefered over the other.
3. Building small projects helps with getting better used to setting up environments, github project, connecting to APIs, getting keys etc
4. Actually building things yourself is very motivating.
3. Cheap models like Haiku are not only fast but the answers are good for task where things need to be looked up. No need to use Sonnet or Opus for such applications as here.