# Periodic architecture review

Every few days, or every few slices, because agents speed up entropy (Pocock, improve-codebase-architecture).

- Look for shallow modules that can be merged, and for modules that have grown too far.
- Check that dependencies point inward and that the domain is still pure.
- Compare names with the glossary. Divergent names are a sign of a confused model.
- Hand the owner a simple diagram of the modules and a short list of proposals. Each proposal has a cost, and says whether it can be reversed.
- Large changes become their own slices on the overall plan, not tidying hidden inside another task.
