# One driver per route

## Key Concept

"Bus factor" is software engineering's bluntest risk metric: how many people can leave
before a system stops. Data and AI estates are full of systems with a bus factor of one -
the nightly revenue ETL, the churn model's retraining loop, the pricing engine's nine years
of exception logic. Leadership decks call this "key person risk" and file it under HR.
It is not an HR problem. It is an operating dependency with a daily departure time.

The tension: an org will happily call something a "production system" - implying service
levels, continuity, ownership - when operationally it is one person's personal knowledge,
leaving the building every evening at 17:31. The org discovers the difference on the day
that person resigns, which is precisely one day too late to do anything about it.

## Explanation

The format is the argument. Instead of illustrating key-person risk, the piece IS the
municipal artifact the metric is named after: a route timetable from the "Knowledge Transit
Authority, Critical Systems Division," played completely straight.

Every mark has one meaning. Routes are critical data/AI systems. The QUALIFIED DRIVERS
column is the bus factor, and the column of 1s is the gut-punch - the eye runs down it and
gets the whole piece in two seconds. The LAST departure is 17:31 for every route, because
that is when the knowledge actually leaves. One route reads 2 with a dagger: the second
driver left in March, the sign was never updated - which is how bus factors decay silently.

The single red accent is spent exactly once: Route 12, PRICING ENGINE, stamped SERVICE
WITHDRAWN - "Sole driver resigned. The route map left with the driver." The row is dimmed
to 0 drivers. This is the resignation that already happened, and it converts the piece from
a joke into a warning.

The deadpan carries the recognition humor: "Route documentation is kept on the bus."
"Handover guides are printed on request, by the driver, from memory." "Replacement service:
an external consultancy operates a limited service at eleven times the standard fare."
Every figure on the artifact is fiction by design - satire register, no invented statistics
presented as fact.

The closing municipal notice is the takeaway, set like a service announcement:
**a route only one person can drive is not a service. It is a favour.**

The reusable taste distinction: **when a concept is named after an object, consider building
the object.** "Bus factor drawn as an actual bus timetable" does what no diagram of the
concept could - the metaphor stops being decoration and becomes the information architecture.

## Recipe

Design-built, no diffusion - the piece is exact type, rules and tabular numerals, which is
diffusion's weakest surface. Hand-authored HTML/CSS (`poster.html`), rendered with headless
Chrome at 1000x1250, device scale 2 (2000x2500 final).

Register: municipal print. Paper cream ground `#F4F1E6`, near-black ink `#191713`, signage
yellow `#F5C518` for the authority band (register realism - it carries no data meaning),
and one meaning accent, withdrawal red `#C2372B`, used only on the stamp and the two red
notices that echo it. Type: Archivo Black for the masthead, Archivo Narrow for the sheet,
IBM Plex Mono for times, form numbers and small print. The stamp is rotated -3.5deg and
allowed to overlap the ruled columns, because real stamps do not respect tables.
